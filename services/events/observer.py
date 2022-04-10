from abc import ABC, abstractmethod


from shigoto_q.integrations.tasks import execute_discord_webhook


class Observer(ABC):
    @abstractmethod
    def execute(
        self,
        url: str,
        title: str,
        description: str,
        color: str,
        embed_url: str,
        footer: str,
    ) -> None:
        pass
