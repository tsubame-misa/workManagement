import os
from discord import Intents, Client, Interaction
from dotenv import load_dotenv
from discord.app_commands import CommandTree
from work import startWork, stopWork, formatDate
load_dotenv()


class MyClient(Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self):
        print(f"login: {self.user.name} [{self.user.id}]")


intents = Intents.default()
client = MyClient(intents=intents)


@client.tree.command()
async def start(interaction: Interaction):
    time = startWork(interaction.user)
    await interaction.response.send_message(f'start, {interaction.user.mention},{formatDate(time)}')


@client.tree.command()
async def stop(interaction: Interaction):
    log = stopWork(interaction.user)
    if log is None:
        await interaction.response.send_message(f'stop, {interaction.user.mention},作業が開始されていません')
        return
    await interaction.response.send_message(f'stop, {interaction.user.mention},終了時刻：{formatDate(log["end_time"])},今回の作業時間：{log["work_time"]}, 合計作業時間：{log["total_time"]}')


client.run(os.getenv("TOKEN"))
