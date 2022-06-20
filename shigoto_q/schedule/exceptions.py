class ScheduleBaseException(Exception):
    pass


class AtleastOneScheduleError(ScheduleBaseException):
    pass


class MultipleSchedulesSetError(ScheduleBaseException):
    pass
