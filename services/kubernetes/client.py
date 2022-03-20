import logging

from django.conf import settings
from kubernetes import client, config, watch

from services.kubernetes.constants import KubernetesEventType
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
