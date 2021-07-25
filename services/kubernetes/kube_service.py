from kubernetes import client, config, watch


def initialize_client():
    config.load_kube_config()

    bv1 = client.BatchV1Api()

    return bv1


def create_docker_image(image, repo_url, full_name):
    pass


def configure_job(name, image, command):
    container = client.V1Container(name=name, image=image, command=command)
    print("container")
    print(container)

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
    )

    spec = client.V1JobSpec(template=template, backoff_limit=4)

    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec,
    )

    return job


def create_job(api_instance, job):
    print("Creating job...")
    api_response = api_instance.create_namespaced_job(body=job, namespace="default")
    print("Job created. status='%s'" % str(api_response.status))


def watch_job(job, namespace):
    label = job.spec.template.metadata.labels
    config.load_kube_config()
    w = watch.Watch()
    core_v1 = client.CoreV1Api()

    job_running = False
    for event in w.stream(
        func=core_v1.list_namespaced_pod,
        namespace=namespace,
        label_selector="{}={}".format(list(label.keys())[0], list(label.values())[0]),
        timeout_seconds=60,
    ):
        if event["object"].status.phase == "Running":
            print("Job running!")
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
        label_selector="{}={}".format(list(label.keys())[0], list(label.values())[0]),
        timeout_seconds=60,
    ):
        if event["object"].status.phase == "Succeeded":
            print("Job succesfully completed!")
            return "SUCCESS"
        print(event["object"].status.phase)


def run_job(name, image, command):
    bv1 = initialize_client()
    job = configure_job(name, image, command)
    create_job(bv1, job)
    watch_job(job, "default")
