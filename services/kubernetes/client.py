import logging

from django.conf import settings
from kubernetes import client, config, watch

from services.kubernetes.constants import (
    KubernetesEventType,
    KubernetesKindTypes,
    LABELS,
    METADATA_NAME,
    NAMESPACE,
    DEFAULT_PORT,
    KubernetesApiVersions,
    DEFAULT_HOST,
    KubernetesImagePullPolicy,
)
from services.kubernetes.exceptions import (
    KubernetesJobNotFoundError,
    KubernetesServiceError,
)

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[KUBERNETES-SERVICE]"


class KubernetesService:
    created_job = None

    def __init__(self):
        config.load_kube_config()
        self.core_v1_api = client.CoreV1Api()

    @classmethod
    def create_job(cls, task_name: str, image_name: str, command: str):
        logger.info(
            f"{_LOG_PREFIX} Creating job with name: {task_name} and image name: {image_name}"
        )
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=task_name),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": task_name}),
                    spec=client.V1PodSpec(
                        restart_policy="Never",
                        containers=[
                            client.V1Container(
                                name=task_name,
                                image=settings.DOCKER_IMAGE_PREFIX + "/" + image_name,
                                command=command,
                            )
                        ],
                    ),
                ),
                backoff_limit=4,
            ),
        )
        api_response = client.BatchV1Api().create_namespaced_job(
            body=job, namespace="default"
        )
        logger.info(f"{_LOG_PREFIX} Job created. status={str(api_response.status)}")
        cls.created_job = job.spec.template.metadata.labels

    @classmethod
    def watch_job(cls, namespace: str = "default"):
        if cls.created_job is None:
            raise KubernetesJobNotFoundError("Cannot watch job that's not yet created.")
        logger.info(f"{_LOG_PREFIX} Starting job watcher.")
        label = cls.created_job.spec.template.metadata.labels
        config.load_kube_config()
        w = watch.Watch()
        core_v1 = client.CoreV1Api()

        job_running = False
        for event in w.stream(
            func=core_v1.list_namespaced_pod,
            namespace=namespace,
            label_selector="{}={}".format(
                list(label.keys())[0], list(label.values())[0]
            ),
            timeout_seconds=60,
        ):
            if event["object"].status.phase != KubernetesEventType.PENDING.value:
                job_running = True
                w.stop()

            if event["type"] == KubernetesEventType.DELETE.value:
                logger.info(f"{_LOG_PREFIX} Job was deleted before startup.")
                w.stop()

        if job_running:
            pod_name = (
                core_v1.list_namespaced_pod(
                    namespace=namespace,
                    label_selector="{}={}".format(
                        list(label.keys())[0], list(label.values())[0]
                    ),
                )
                .items[0]
                .metadata.name
            )
            w = watch.Watch()
            for _ in w.stream(
                func=core_v1.read_namespaced_pod_log,
                name=pod_name,
                namespace=namespace,
            ):
                pass

        w = watch.Watch()
        for event in w.stream(
            func=core_v1.list_namespaced_pod,
            namespace=namespace,
            label_selector="{}={}".format(
                list(label.keys())[0], list(label.values())[0]
            ),
            timeout_seconds=60,
        ):
            if event["object"].status.phase == KubernetesEventType.SUCCEEDED.value:
                logger.info(f"{_LOG_PREFIX} Job successfully completed!")
                break

    @classmethod
    def _create_kubernetes_object_meta(cls, service_name: str = None, **kwargs: dict):
        return client.V1ObjectMeta(
            name=service_name,
            **kwargs,
        )

    def create_namespace(self, name: str):
        return self.core_v1_api.create_namespace(
            body={
                "apiVersion": KubernetesApiVersions.API_VERSION.value,
                "kind": KubernetesKindTypes.NAMESPACE.value,
                "metadata": {
                    "name": name,
                    "resourceversion": KubernetesApiVersions.API_VERSION.value,
                },
            }
        )

    @classmethod
    def _create_deployment(
        cls,
        apps_v1_api: client.AppsV1Api,
        name: str,
        image: str,
        port: int,
        pull_policy: str = KubernetesImagePullPolicy.ALWAYS.value,
        replicas: int = 1,
        label_selector: dict = LABELS,
        namespace: str = 'default',
    ):
        logger.info(
            f"{_LOG_PREFIX} Creating kubernetes deployment with name={name} and image={image}"
        )
        container = client.V1Container(
            name=name,
            image=image,
            image_pull_policy=pull_policy,
            ports=[client.V1ContainerPort(container_port=port)],
        )
        template = client.V1PodTemplateSpec(
            metadata=cls._create_kubernetes_object_meta(**dict(labels=label_selector)),
            spec=client.V1PodSpec(containers=[container]),
        )
        spec = client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels=label_selector),
            template=template,
        )
        deployment = client.V1Deployment(
            api_version=KubernetesApiVersions.APPS_API_VERSION.value,
            kind=KubernetesKindTypes.DEPLOYMENT.value,
            metadata=cls._create_kubernetes_object_meta(service_name=name),
            spec=spec,
        )
        resp = apps_v1_api.create_namespaced_deployment(
            namespace=namespace,
            body=deployment,
        )
        return resp

    @classmethod
    def _create_spec_ports(cls, port: int, target_port: int):
        return client.V1ServicePort(
            port=port,
            target_port=target_port,
        )

    @classmethod
    def create_load_balancer(
        cls,
        core_v1_api: client.CoreV1Api,
        port: int,
        target_port: int,
        name: str,
        selector_label: dict = LABELS,
    ):
        service = client.V1Service(
            api_version=KubernetesApiVersions.API_VERSION.value,
            kind=KubernetesKindTypes.SERVICE.value,
            metadata=cls._create_kubernetes_object_meta(name),
            spec=client.V1ServiceSpec(
                selector=selector_label,
                ports=[cls._create_spec_ports(port, target_port)],
                type="",
            ),
        )
        return service

    def _create_service(
        self,
        service_name: str,
        port: int,
        target_port: int,
        namespace,
        label_selector: dict = LABELS,
    ):
        logger.info(
            f"{_LOG_PREFIX} Creating kubernetes service(name={service_name}, namespace={NAMESPACE})."
        )
        body = client.V1Service(
            api_version=KubernetesApiVersions.API_VERSION.value,
            kind=KubernetesKindTypes.SERVICE.value,
            metadata=self._create_kubernetes_object_meta(service_name),
            spec=client.V1ServiceSpec(
                selector=label_selector,
                ports=[
                    client.V1ServicePort(
                        port=port,
                        target_port=target_port,
                    )
                ],
            ),
        )
        return self.core_v1_api.create_namespaced_service(
            namespace=namespace,
            body=body,
        )

    @classmethod
    def _create_ingress(
        cls,
        networking_v1_api: client.NetworkingV1Api,
        name: str,
        host: str = DEFAULT_HOST,
        namespace: str = NAMESPACE,
    ):
        logger.info(f"{_LOG_PREFIX} Creating Ingress for host={host}")
        body = client.V1Ingress(
            api_version=KubernetesApiVersions.INGRESS_API_VERSION.value,
            kind=KubernetesKindTypes.INGRESS.value,
            metadata=cls._create_kubernetes_object_meta(
                service_name=name,
                **{
                    "annotations": {
                        "nginx.ingress.kubernetes.io/rewrite-target": "/",
                    }
                },
            ),
            spec=client.V1IngressSpec(
                rules=[
                    client.V1IngressRule(
                        host=host,
                        http=client.V1HTTPIngressRuleValue(
                            paths=[
                                client.V1HTTPIngressPath(
                                    path="/",
                                    path_type="Exact",
                                    backend=client.V1IngressBackend(
                                        service=client.V1IngressServiceBackend(
                                            port=client.V1ServiceBackendPort(
                                                number=DEFAULT_PORT,
                                            ),
                                            name=name,
                                        )
                                    ),
                                )
                            ]
                        ),
                    )
                ]
            ),
        )

        networking_v1_api.create_namespaced_ingress(
            namespace=namespace,
            body=body,
        )

    def create_service(self, service_name, port, target_port, namespace, user_id):
        logger.info(
            f"{_LOG_PREFIX} User(id={user_id}) is creating new kubernetes service."
        )
        return self._create_service(
            service_name=service_name,
            port=port,
            target_port=target_port,
            namespace=namespace,
        )

    @classmethod
    def create_deployment(cls, user_id, name, image, namespace, port):
        config.load_kube_config()
        logger.info(
            f"{_LOG_PREFIX} User(id={user_id}) is creating new kubernetes deployment."
        )
        apps_v1_api = client.AppsV1Api()
        try:
            return cls._create_deployment(
                apps_v1_api=apps_v1_api,
                name=name,
                image=image,
                namespace=namespace,
                port=port,
            )
        except Exception as e:
            raise KubernetesServiceError(f"{_LOG_PREFIX} {str(e)}")

    def delete_namespace(self, name: str):
        self.core_v1_api.delete_namespace(name=name)
