from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client, config
from google.cloud import storage
from google.oauth2 import service_account
import glob
import os
from google.auth import compute_engine





def initialize_client():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    bv1 = client.BatchV1Api()

    return v1, bv1



def configure_job(name, image, command):
    container = client.V1Container(
        name=name,
        image=image,
        command=command)

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))

    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)

    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return job

def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace="default")
    print("Job created. status='%s'" % str(api_response.status))

def run_job(name, image, command):
    v1, bv1 = initialize_client()
    job = configure_job()
    create_job(bv1, job)








