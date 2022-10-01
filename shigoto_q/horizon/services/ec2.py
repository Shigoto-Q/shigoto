from services.aws import ec2 as aws_services
from services.aws import types as aws_types
from shigoto_q.horizon import models as horizon_models
from shigoto_q.horizon import enums as horizon_enums


ec_client = aws_services.EC2Client()


def create_and_launch_instance(data: dict, user_id: int):
    ebs_desc = aws_types.EbsDesc.from_dict(data=data)
    block_desc = aws_types.EC2InstanceBlockDesc.from_dict(data=data, ebs=ebs_desc)
    placement_desc = aws_types.PlacementDesc.from_dict(data=data)
    instance_desc = aws_types.EC2InstanceDesc.from_dict(
        data=data,
        block=block_desc,
        placement=placement_desc,
    )

    response = ec_client.launch(instance_desc=instance_desc)
    instances = response["Instances"]
    if instances:
        instance = instances[0]
        network = horizon_models.Network(
            private_ipv4_dns=instance["PrivateDnsName"],
            private_ipv4_address=instance["PrivateIpAddress"],
            public_ipv4_dns=instance["PublicDnsName"],
            subnet_id=instance["SubnetId"],
            vpc_id=instance["VpcId"],
            owner_id=user_id,
        )
        network.save()
        virtual_machine = horizon_models.VirtualMachine(
            instance_id=instance["InstanceId"],
            launch_time=instance["LaunchTime"],
            image_id=instance["InstanceId"],
            state=horizon_enums.InstanceState.from_response(instance["State"]["Name"]),
            owner_id=user_id,
        )
        virtual_machine.save()
