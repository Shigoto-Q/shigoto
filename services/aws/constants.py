import enum


class InstanceType(enum.Enum):
    T2_MICRO = 't2.micro'


class VolumeType(enum.Enum):
    STANDARD = 'standard'
    IO1 = 'io1'
    IO2 = 'io2'

    CS1 = 'cs1'
    ST1 = 'st1'

    GP2 = 'gp2'
    GP3 = 'gp3'


class Tenancy(enum.Enum):
    DEFAULT = 'default'
    DEDICATED = 'dedicated'
    HOST = 'host'
