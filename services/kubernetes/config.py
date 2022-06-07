import yaml

from kubernetes import client
from kubernetes.client import Configuration
from kubernetes.config import kube_config


class KubernetesConfig:
    def __init__(self, configuration_yaml):
        self.configuration_yaml = configuration_yaml
        self._configuration_yaml = None

    @property
    def config(self):
        with open(self.configuration_yaml, "r") as f:
            if self._configuration_yaml is None:
                self._configuration_yaml = yaml.load(f)
        return self._configuration_yaml

    @property
    def client(self):
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.CoreV1Api()


# # Instantiate your kubernetes class and pass in config
# kube_one = K8s(configuration_yaml='~/.kube/config1')
# kube_one.client.list_pod_for_all_namespaces(watch=False)
#
# kube_two = K8s(configuration_yaml='~/.kube/config2')
# kube_two.client.list_pod_for_all_namespaces(watch=False)
