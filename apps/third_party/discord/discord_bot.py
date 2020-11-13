import discord

from apps.third_party.discord.command.discord_command_helper import stock_price, is_users_order, help_text, stock_subscribe, current_stock_subscribe_list
from apps.third_party.discord.discord_settings import DISCORD_TOKEN

"""
cd /home/django_sample
python -m apps.third_party.discord.discord_bot
"""


class DiscordBot(discord.Client):

    async def on_ready(self):
        print('[Start]', self.user)

    async def on_message(self, message):
        user_message = message.content.split()

        if await is_users_order(user_message):
            user_message, *etc_message = user_message[0].replace('!', ''), user_message[1:]

            if user_message == 'help':
                await message.channel.send(await help_text())

            elif user_message == '구독리스트':
                await message.channel.send(await current_stock_subscribe_list())

            elif user_message == '구독':
                await message.channel.send(await stock_subscribe(etc_message[0][0]))

            else:
                await message.channel.send(await stock_price(user_message))


client = DiscordBot()
client.run(DISCORD_TOKEN)
