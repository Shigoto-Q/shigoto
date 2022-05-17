from django.db import models


class KubernetesKinds(models.IntegerChoices):
    DEPLOYMENT = 0
    SERVICE = 1
    INGRESS = 2


class KubernetesServiceTypes(models.IntegerChoices):
    CLUSTER_IP = 0
    LOAD_BALANCER = 1
    NODE_PORT = 2
