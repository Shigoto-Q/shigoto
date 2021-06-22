from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = "shigoto_q.tasks"
    verbose_name = "Tasks"

    def ready(self):
        try:
            import shigoto_q.tasks.signals
        except ImportError:
            pass
