import os
from discord import app_commands, Intents, Client, Interaction
from dotenv import load_dotenv
from discord.app_commands import CommandTree
from discord.ui import Select, View
from work import startWork, stopWork
from error import NoStartError, WorkingError, ApiError
from help import getHelpText
from api import getUserProjects
from common import formatDate
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
@app_commands.describe(project="what project?")
async def start(
    interaction: Interaction,
    project: str,
):
    time = None
    try:
        time = startWork(interaction.user, project)
        time = formatDate(time)
    except WorkingError:
        await interaction.response.send_message(f'start {project} \n このプロジェクトは作業中です')
        return
    except ApiError:
        await interaction.response.send_message(f'start {project} \n 保存処理の最中にエラーが発生しました')
        return

    await interaction.response.send_message(f'start {project} {interaction.user.mention} \n 開始時刻 {time}')


@client.tree.command()
@app_commands.describe(project="what project?")
async def stop(interaction: Interaction, project: str,):
    log = None

    try:
        log = stopWork(interaction.user, project)
    except NoStartError:
        await interaction.response.send_message(f'stop {project} {interaction.user.mention} \n 作業が開始されていません')
        return
    except ApiError:
        await interaction.response.send_message(f'stop {project} \n 保存処理の最中にエラーが発生しました')
        return

    await interaction.response.send_message(f'stop {project} {interaction.user.mention} \n 終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')


@client.tree.command()
async def projects(interaction: Interaction):
    projects = None

    try:
        projects = getUserProjects(interaction.user)
    except ApiError:
        await interaction.response.send_message(f'projects  \n 保存処理の最中にエラーが発生しました')
        return

    if len(projects) == 0:
        await interaction.response.send_message(f'projects {interaction.user.mention} \n プロジェクトは作成されていません')
        return
    await interaction.response.send_message(f'project {interaction.user.mention} \n {projects}')


@client.tree.command()
async def help(interaction: Interaction):
    msg = getHelpText()
    await interaction.response.send_message(f'help {interaction.user.mention} \n {msg}')


client.run(os.getenv("TOKEN"))
