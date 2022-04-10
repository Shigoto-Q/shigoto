import logging

from django.conf import settings
from kubernetes import client, config, watch

from services.kubernetes.constants import (
    KubernetesEventType,
    KubernetesKindTypes,
    LABELS,
    METADATA_NAME,
    API_VERSION,
    NAMESPACE,
    DEFAULT_PORT,
    KubernetesApiVersions,
    DEFAULT_HOST,
)
from services.kubernetes.exceptions import KubernetesJobNotFoundError

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[KUBERNETES-SERVICE]"


class KubernetesService:
    created_job = None

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
            for event in w.stream(
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
    def _create_deployment(
        cls,
        apps_v1_api: client.AppsV1Api,
        name: str,
        image: str,
        pull_policy: str = "Never",
    ):
        container = client.V1Container(
            name=name,
            image=image,
            image_pull_policy=pull_policy,
            ports=[client.V1ContainerPort(container_port=DEFAULT_PORT)],
        )
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=LABELS),
            spec=client.V1PodSpec(containers=[container]),
        )
        spec = client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels=LABELS),
            template=template,
        )
        deployment = client.V1Deployment(
            api_version=KubernetesApiVersions.APPS_API_VERSION.value,
            kind=KubernetesKindTypes.DEPLOYMENT.value,
            metadata=client.V1ObjectMeta(name=METADATA_NAME),
            spec=spec,
        )
        apps_v1_api.create_namespaced_deployment(
            namespace=NAMESPACE,
            body=deployment,
        )

    @classmethod
    def _create_service(cls, service_name: str, namespace: str = NAMESPACE):
        core_v1_api = client.CoreV1Api()
        body = client.V1Service(
            api_version=KubernetesApiVersions.API_VERSION.value,
            kind=KubernetesKindTypes.SERVICE.value,
            metadata=client.V1ObjectMeta(
                name=service_name,
            ),
            spec=client.V1ServiceSpec(
                selector=LABELS,
                ports=[
                    client.V1ServicePort(
                        port=DEFAULT_PORT,
                        target_port=DEFAULT_PORT,
                    )
                ],
            ),
        )
        core_v1_api.create_namespaced_service(
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
        body = client.V1Ingress(
            api_version=KubernetesApiVersions.INGRESS_API_VERSION.value,
            kind=KubernetesKindTypes.INGRESS.value,
            metadata=client.V1ObjectMeta(
                name=name,
                annotations={
                    "nginx.ingress.kubernetes.io/rewrite-target": "/",
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

    @classmethod
    def create_deployment_and_ingress(
        cls,
        name: str,
        image: str,
        service_name: str,
        host: str,
    ):
        apps_v1_api = client.AppsV1Api()
        networking_v1_api = client.NetworkingV1Api()

        cls._create_deployment(
            apps_v1_api=apps_v1_api,
            name=name,
            image=image,
        )
        cls._create_service(service_name=service_name)
        cls._create_ingress(
            networking_v1_api=networking_v1_api,
            name=name,
            host=host,
        )
