from config import celery_app
from services.discord import client as discord_client


@celery_app.task()
def execute_discord_webhook(
    url: str,
    title: str,
    description: str,
    color: str,
    embed_url: str,
    footer: str,
):
    webhook = discord_client.DiscordWebhook(url=url)
    embed = discord_client.DiscordEmbed(
        title=title, description=description, color=color
    )
    embed.set_url(embed_url)
    embed.set_footer(text=footer)
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
