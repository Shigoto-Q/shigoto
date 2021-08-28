from __future__ import absolute_import

import json
import typing
import requests

from kubernetes import client, config, watch

from django.conf import settings


class ImageService:
    def create_image(self, repo_url, full_name, image_name):
        res = requests.post(
            settings.DOCKER_IMAGE_SERVICE,
            json={
                "repo_url": repo_url,
                "full_name": full_name,
                "image_name": image_name,
            },
        )
        return res


class KubernetesService:
    """
    kubernetes class to create and start job
    """

    def __init__(
        self,
        repo_url: str,
        full_name: str,
        image_name: str,
        command: typing.List[str],
        user: int,
        task_name: str,
    ):
        config.load_kube_config()
        self._api_instance = client.BatchV1Api()
        self.repo_url = repo_url
        self.image_name = image_name
        self.full_name = full_name
        self.command = ["echo", "looool"]
        self.user = user
        self.task_name = task_name
        self._job = None
        self.image_prefix = "bogdanp3trovic"

    def _configure_job(self):
        print(self.command)
        container = client.V1Container(
            name=self.task_name,
            image=self.image_prefix + "/" + self.image_name,
            command=self.command,
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": self.task_name}),
            spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
        )

        spec = client.V1JobSpec(template=template, backoff_limit=4)
        return client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=self.task_name),
            spec=spec,
        )

    def create_job(self):
        self._job = self._configure_job()
        api_response = self._api_instance.create_namespaced_job(
            body=self._job, namespace="default"
        )
        print(f"Job created. status={str(api_response.status)}")

    def watch_job(self, namespace: str = "default"):
        label = self._job.spec.template.metadata.labels
        print(label)
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
            if event["object"].status.phase != "Pending":
                job_running = True
                w.stop()

            # event.type: ADDED, MODIFIED, DELETED
            if event["type"] == "DELETED":
                # Pod was deleted while we were waiting for it to start.
                print("Job was deleted before startup.")
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
                # send websocket
                print(event)

        w = watch.Watch()
        for event in w.stream(
            func=core_v1.list_namespaced_pod,
            namespace=namespace,
            label_selector="{}={}".format(
                list(label.keys())[0], list(label.values())[0]
            ),
            timeout_seconds=60,
        ):
            if event["object"].status.phase == "Succeeded":
                print("Job succesfully completed!")
                return "SUCCESS"
            print(event["object"].status.phase)
