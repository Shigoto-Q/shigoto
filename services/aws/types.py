from dataclasses import dataclass

from typing import List

from services.aws.constants import VolumeType, InstanceType, Tenancy


@dataclass(frozen=True)
class EbsDesc:
    delete_on_termination: bool
    volume_size: int
    volume_type: VolumeType
    throughput: str
    encrypted: bool


@dataclass(frozen=True)
class EC2InstanceBlockDesc:
    device_name: str
    virtual_name: str
    ebs: EbsDesc
    no_device: str


@dataclass(frozen=True)
class PlacementDesc:
    availability_zone: str
    affinity: str
    group_name: str
    partition_number: int
    host_id: str
    tenancy: Tenancy
    spread_domain: str
    host_resource_group_arn: str


@dataclass(frozen=True)
class EC2InstanceDesc:
    block_device_mapping: EC2InstanceBlockDesc
    placement: PlacementDesc
    image_id: str
    instance_type: InstanceType
    ipv6_address_count: int
    ipv6_addresses: list
    kernel_id: str
    key_name: str
    max_count: int
    min_count: int
    monitoring: bool


@dataclass(frozen=True)
class TerminationDesc:
    instance_ids: List[str]
