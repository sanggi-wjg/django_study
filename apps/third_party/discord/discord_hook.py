import json
import requests

from apps.third_party.discord.discord_settings import DISCORD_RSI_HOOK


def send_discord(content: str):
    requests.post(
        url = DISCORD_RSI_HOOK,
        data = json.dumps({
            'content': content
        }),
        headers = {
            'Content-Type': 'application/json',
        }
    )
