import os
from discord import app_commands, Intents, Client, Interaction, File, Embed
from dotenv import load_dotenv
from discord.app_commands import CommandTree, Choice
from work import startWork, stopWork, getUserProjectsText
from error import NoStartError, WorkingError, ApiError, NoFinishedError
from help import getCommandDetail
from common import formatDate
from log import makeLogFile
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
@app_commands.describe(project="プロジェクト名", description="作業内容(任意)")
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
        await interaction.followup.send(f'start {project} \nこのプロジェクトは作業中です。')
        return
    except ApiError:
        await interaction.followup.send(f'start {project} \n保存処理の最中にエラーが発生しました。管理者に問い合わせて下さい。')
        return
    except NoFinishedError:
        await interaction.followup.send(f'start {project} \nこのプロジェクトには終了されていない作業があります。管理者に問い合わせて下さい。')
        return

    if description is None:
        await interaction.followup.send(f'start {project} {interaction.user.mention} \n開始時刻 {time}')
    else:
        await interaction.followup.send(f'start {project}:{description} {interaction.user.mention} \n開始時刻 {time}')


@client.tree.command()
@app_commands.describe(project="プロジェクト名")
async def stop(interaction: Interaction, project: str):
    log = None
    try:
        log = stopWork(interaction.user, project)
    except NoStartError:
        await interaction.response.send_message(f'stop {project} {interaction.user.mention} \n作業が開始されていません。')
        return
    except ApiError:
        await interaction.response.send_message(f'stop {project} \n保存処理の最中にエラーが発生しました。管理者に問い合わせて下さい。')
        return
    except NoFinishedError:
        await interaction.response.send_message(f'stop {project} \nこのプロジェクトには終了されていない作業があります。管理者に問い合わせて下さい。')
        return

    if log["description"] is None:
        await interaction.response.send_message(f'stop {project} {interaction.user.mention} \n終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')
    else:
        await interaction.response.send_message(f'stop {project}:{log["description"]} {interaction.user.mention} \n終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')


@client.tree.command()
async def projects(interaction: Interaction):
    projects = None

    try:
        projects = getUserProjectsText(interaction.user)
    except ApiError:
        await interaction.response.send_message(f'projects  \n保存処理の最中にエラーが発生しました')
        return

    if len(projects) == 0:
        await interaction.response.send_message(f'projects {interaction.user.mention} \nプロジェクトは作成されていません')
        return
    await interaction.response.send_message(f'project {interaction.user.mention} \n{projects}')


@client.tree.command(name="help")
@app_commands.describe(commands="コマンド名(任意)")
@app_commands.choices(commands=[
    Choice(name="start", value="start"),
    Choice(name="stop", value="stop"),
    Choice(name="projects", value="projects"),
    Choice(name="download_file", value="download_file"),
])
async def help(interaction: Interaction, commands: Choice[str] = None):
    if commands is None:
        embed = Embed(title="work management bot commands",
                      description="`/help <command_name>` で詳細を見ることができます。", color=0x2daffa)
        embed.add_field(name="`/start <project_name> <description>` ",
                        value="作業の開始")
        embed.add_field(name="`/stop <project_name>`", value="作業の終了\n")
        embed.add_field(name="`/projects`", value="プロジェクト作業時間の一覧表示\n")
        embed.add_field(name="`/download_file`",
                        value="プロジェクトの詳細データ(json)のダウンロード")
        await interaction.response.send_message(embed=embed)
    else:
        try:
            command_detail = getCommandDetail(commands.value)
            embed = Embed(title="",
                          description="", color=0x2daffa)
            embed.add_field(name=command_detail["name"],
                            value=command_detail["value"])
            await interaction.response.send_message(embed=embed)
        except KeyError:
            await interaction.response.send_message(f'コマンド {commands.name} はwork managemantに存在しません')


@client.tree.command()
async def download_file(interaction: Interaction):
    try:
        filepath = makeLogFile(interaction.user)
    except:
        await interaction.response.send_message("エラーが発生しました。管理者に問い合わせて下さい。")
        return

    await interaction.response.send_message(file=File(filepath))

client.run(os.getenv("TOKEN"))
