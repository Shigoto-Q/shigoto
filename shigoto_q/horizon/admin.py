from django.contrib import admin

from shigoto_q.horizon.models import Database, VirtualMachine, Volume, Network


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'engine',
        'host',
        'port',
        'name',
        'username',
        'password',
    )
    search_fields = ('name',)


@admin.register(VirtualMachine)
class VirtualMachineAdmin(admin.ModelAdmin):
    list_display = (
        'instance_id',
        'name',
        'description',
        'operating_system',
        'type',
        'state',
        'launch_time',
        'owner',
        'created',
        'updated',
        'volume',
        'network',
    )
    list_filter = (
        'launch_time',
        'owner',
        'created',
        'updated',
        'volume',
        'network',
    )
    search_fields = ('name',)


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'device_name',
        'attachment_status',
        'attachment_time',
        'encrypted',
        'size',
        'created',
        'updated',
        'owner',
    )
    list_filter = (
        'attachment_time',
        'encrypted',
        'created',
        'updated',
        'owner',
    )


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = (
        'interface_id',
        'description',
        'availability_zone',
        'public_ipv4_dns',
        'public_ipv4_address',
        'private_ipv4_dns',
        'private_ipv4_address',
        'public_ipv6_address',
        'vpc_id',
        'subnet_id',
        'owner',
    )
    list_filter = ('owner',)
