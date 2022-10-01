from __future__ import annotations

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

    @classmethod
    def from_dict(cls, data: dict) -> EbsDesc:
        return cls(
            delete_on_termination=data.get("delete_on_termination"),
            volume_size=data.get("volume_size"),
            volume_type=data.get("volume_type"),
            throughput=data.get("throughput", ""),
            encrypted=data.get("encrypted"),
        )


@dataclass(frozen=True)
class EC2InstanceBlockDesc:
    device_name: str
    virtual_name: str
    ebs: EbsDesc
    no_device: str

    @classmethod
    def from_dict(cls, data: dict, ebs: EbsDesc) -> EC2InstanceBlockDesc:
        return cls(
            device_name=data.get("device_name"),
            virtual_name=data.get("virtual_name"),
            ebs=ebs,
            no_device=data.get("no_device", ""),
        )


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

    @classmethod
    def from_dict(cls, data: dict) -> PlacementDesc:
        return cls(
            availability_zone=data.get("availability_zone"),
            affinity=data.get("affinity"),
            group_name=data.get("group_name"),
            partition_number=data.get("partition_number"),
            host_id=data.get("host_id"),
            tenancy=data.get("tenancy"),
            spread_domain=data.get("spread_domain"),
            host_resource_group_arn=data.get("host_resource_group_arn"),
        )


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

    @classmethod
    def from_dict(
        cls, data: dict, block: EC2InstanceBlockDesc, placement: PlacementDesc
    ) -> EC2InstanceDesc:
        return cls(
            block_device_mapping=block,
            placement=placement,
            image_id=data.get("image_id"),
            instance_type=data.get("instance_type"),
            ipv6_address_count=data.get("ipv6_address_count"),
            ipv6_addresses=data.get("ipv6_addresses"),
            kernel_id=data.get("kernel_id", ""),
            key_name=data.get("key_name"),
            min_count=data.get("min_count", 1),
            max_count=data.get("max_count"),
            monitoring=data.get("monitoring", False),
        )


@dataclass(frozen=True)
class TerminationDesc:
    instance_ids: List[str]
