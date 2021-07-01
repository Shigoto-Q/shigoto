from kubernetes import client, config
import git
from google.cloud import storage
from google.oauth2 import service_account
import glob
import os
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client


def upload_local_directory_to_gcs(local_path, bucket, gcs_path):
    assert os.path.isdir(local_path)
    for local_file in glob.glob(local_path + '/**'):
        if not os.path.isfile(local_file):
            upload_local_directory_to_gcs(local_file, bucket, gcs_path + "/" + os.path.basename(local_file))
        else:
            remote_path = os.path.join(gcs_path, local_file[1 + len(local_path):])
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)


def initialize_client():
    project_id = "tough-canto-314909"
    zone = "europe-west1-b"
    cluster_id = "cluster-1"
    credentials = service_account.Credentials.from_service_account_file(
        "C:/Users/bogda/OneDrive/Desktop/shegoto/shigoto_q/keyfiles/gke_service_account.json")

    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{cluster_id}')

    configuration = client.Configuration()
    configuration.host =f"https://{cluster.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization" : "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()




def download_repo(repo_url, username):
    git.Git("./").clone("https://github.com/b0gdanp3trovic/test_docker.git")
    credentials = service_account.Credentials.from_service_account_file(
        "C:/Users/bogda/OneDrive/Desktop/shegoto/shigoto_q/keyfiles/gke_service_account.json")
    storage_client = storage.Client(credentials=credentials)
    if username not in storage_client.list_buckets():
        storage_client.create_bucket(username)

    bucket = storage_client.bucket(username)
    upload_local_directory_to_gcs('./test_docker', bucket, '.')


