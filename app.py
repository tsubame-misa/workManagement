import os
from discord import app_commands, Intents, Client, Interaction, File
from dotenv import load_dotenv
from discord.app_commands import CommandTree
from discord.ui import Select, View
from work import startWork, stopWork, getUserProjectsText
from error import NoStartError, WorkingError, ApiError, NoFinishedError
from help import getHelpText
from api import getUserProjects
from common import formatDate
from log import makeLogFile, rmLogFile
import asyncio
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
@app_commands.describe(project="プロジェクト名", description="作業内容")
async def start(
    interaction: Interaction,
    project: str,
    description: str = None,
):
    time = None
    try:
        await interaction.response.defer()
        time = startWork(interaction.user, project, description)
        time = formatDate(time)
    except WorkingError:
        await interaction.followup.send(f'start {project} \n このプロジェクトは作業中です。')
        return
    except ApiError:
        await interaction.followup.send(f'start {project} \n 保存処理の最中にエラーが発生しました。管理者に問い合わせて下さい。')
        return
    except NoFinishedError:
        await interaction.followup.send(f'start {project} \n このプロジェクトには終了されていない作業があります。管理者に問い合わせて下さい。')
        return

    if description is None:
        await interaction.followup.send(f'start {project} {interaction.user.mention} \n 開始時刻 {time}')
    else:
        await interaction.followup.send(f'start {project}:{description} {interaction.user.mention} \n 開始時刻 {time}')


@client.tree.command()
@app_commands.describe(project="プロジェクト名")
async def stop(interaction: Interaction, project: str):
    log = None
    try:
        await interaction.response.defer()
        log = stopWork(interaction.user, project)
    except NoStartError:
        await interaction.followup.send(f'stop {project} {interaction.user.mention} \n 作業が開始されていません。')
        return
    except ApiError:
        await interaction.followup.send(f'stop {project} \n 保存処理の最中にエラーが発生しました。管理者に問い合わせて下さい。')
        return
    except NoFinishedError:
        await interaction.followup.send(f'stop {project} \n このプロジェクトには終了されていない作業があります。管理者に問い合わせて下さい。')
        return

    if log["description"] is None:
        await interaction.followup.send(f'stop {project} {interaction.user.mention} \n 終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')
    else:
        await interaction.followup.send(f'stop {project}:{log["description"]} {interaction.user.mention} \n 終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')


@client.tree.command()
async def projects(interaction: Interaction):
    projects = None

    try:
        projects = getUserProjectsText(interaction.user)
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


@client.tree.command()
async def download_file(interaction: Interaction):
    filepath = makeLogFile(interaction.user)
    await interaction.response.send_message(file=File(filepath))


@client.tree.command()
async def defer(interaction: Interaction):

    await interaction.response.defer()
    await asyncio.sleep(3)
    # await interaction.response.send_message("fin")
    await interaction.followup.send("hoge")
    # await interaction.response.send_message("fin", ephemeral=True)


client.run(os.getenv("TOKEN"))
