import logging

import boto3

from services.aws.types import EC2InstanceDesc, TerminationDesc


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[EC2-CLIENT]"


class EC2Client:
    def __init__(self, dry_run=False, region_name: str = "us-east-1"):
        self.client = boto3.client("ec2", region_name=region_name)
        self.dry_run = dry_run

    def launch(self, instance_desc: EC2InstanceDesc):
        logger.info(f"{_LOG_PREFIX} Launching EC2 Instance: {instance_desc}")
        response = self.client.run_instances(
            BlockDeviceMappings=[
                {
                    "DeviceName": instance_desc.block_device_mapping.device_name,
                    "VirtualName": instance_desc.block_device_mapping.virtual_name,
                    "Ebs": {
                        "DeleteOnTermination": instance_desc.block_device_mapping.ebs.delete_on_termination,
                        "VolumeSize": instance_desc.block_device_mapping.ebs.volume_size,
                        "VolumeType": instance_desc.block_device_mapping.ebs.volume_type.value,
                        "Encrypted": instance_desc.block_device_mapping.ebs.encrypted,
                    },
                },
            ],
            ImageId=instance_desc.image_id,
            InstanceType=instance_desc.instance_type.value,
            Ipv6AddressCount=instance_desc.ipv6_address_count,
            KeyName=instance_desc.key_name,
            MinCount=instance_desc.min_count,
            MaxCount=instance_desc.max_count,
            Placement={
                "AvailabilityZone": instance_desc.placement.availability_zone,
                "Tenancy": instance_desc.placement.tenancy.value,
            },
            DryRun=self.dry_run,
        )
        return response

    def terminate(self, instances: TerminationDesc):
        logger.info(f"{_LOG_PREFIX} Terminating the following instances: {instances}")
        response = self.client.terminate_instances(
            InstanceIds=instances.instance_ids, DryRun=self.dry_run
        )
        return response
