from services.events.observer import Observer

from shigoto_q.integrations.tasks import execute_discord_webhook


class DeploymentEvent(Observer):
    def execute(
        self,
        url: str,
        title: str,
        description: str,
        color: str,
        embed_url: str,
        footer: str,
    ):
        execute_discord_webhook.apply_async(
            args=[url, title, description, color, embed_url, footer]
        )
        print(f"Executing {url}")


class TaskSuccessEvent(Observer):
    def execute(
        self,
        url: str,
        title: str,
        description: str,
        color: str,
        embed_url: str,
        footer: str,
    ):
        execute_discord_webhook.apply_async(
            args=[url, title, description, color, embed_url, footer]
        )


class TaskFailureEvent(Observer):
    def execute(
        self,
        url: str,
        title: str,
        description: str,
        color: str,
        embed_url: str,
        footer: str,
    ):
        execute_discord_webhook.apply_async(
            args=[url, title, description, color, embed_url, footer]
        )
