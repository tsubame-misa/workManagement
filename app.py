import os
from discord import app_commands, Intents, Client, Interaction, File, Embed, User
from dotenv import load_dotenv
from discord.app_commands import CommandTree, Choice
from work import startWork, stopWork, getUserProjectsText, getUserProjectDetail, getUserProjectDetailText, addViewer
from error import NoStartError, WorkingError, ApiError, NoFinishedError, NoProjectError, AddedError
from help import getCommandDetail
from common import formatDate
from log import makeLogFile
from api import getUserWorkingProjects, getUserNotWorkingProjects, getUserProjects
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
        await interaction.followup.send(f'{project} \nこのプロジェクトは作業中です。')
        return
    except ApiError:
        await interaction.followup.send(f'{project} \n保存処理の最中にエラーが発生しました。管理者に問い合わせて下さい。')
        return
    except NoFinishedError:
        await interaction.followup.send(f'{project} \nこのプロジェクトには終了されていない作業があります。管理者に問い合わせて下さい。')
        return

    if description is None:
        await interaction.followup.send(f'{project} {interaction.user.mention} \n開始時刻 {time}')
    else:
        await interaction.followup.send(f'{project}:{description} {interaction.user.mention} \n開始時刻 {time}')


@client.tree.command()
@app_commands.describe(project="プロジェクト名")
async def stop(interaction: Interaction, project: str):
    log = None
    try:
        await interaction.response.defer()
        log = stopWork(interaction.user, project)
    except NoStartError:
        await interaction.followup.send(f'{project} {interaction.user.mention} \n作業が開始されていません。')
        return
    except ApiError:
        await interaction.followup.send(f'{project} \n保存処理の最中にエラーが発生しました。管理者に問い合わせて下さい。')
        return
    except NoFinishedError:
        await interaction.followup.send(f'{project} \nこのプロジェクトには終了されていない作業があります。管理者に問い合わせて下さい。')
        return

    if log["description"] is None:
        await interaction.followup.send(f'{project} {interaction.user.mention} \n終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')
    else:
        await interaction.followup.send(f'{project}:{log["description"]} {interaction.user.mention} \n終了時刻 {formatDate(log["end_time"])}, 今回の作業時間 {log["work_time"]}, 合計作業時間 {log["total_time"]}')


@client.tree.command()
async def projects(interaction: Interaction):
    projects = None

    try:
        projects = getUserProjectsText(interaction.user)
    except ApiError:
        await interaction.response.send_message(f'保存処理の最中にエラーが発生しました')
        return

    if len(projects) == 0:
        await interaction.response.send_message(f'{interaction.user.mention} \nプロジェクトは作成されていません')
        return
    await interaction.response.send_message(f'{interaction.user.mention} \n{projects}')


@client.tree.command()
async def project_detail(interaction: Interaction, project_name: str):
    projects = None
    try:
        projects = getUserProjectDetailText(interaction.user, project_name)
    except ApiError:
        await interaction.response.send_message(f'保存処理の最中にエラーが発生しました')
        return

    if projects is None:
        await interaction.response.send_message(f'{interaction.user.mention} \nプロジェクトは作成されていません')
        return
    await interaction.response.send_message(f'{interaction.user.mention} \n{projects}')


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


@client.tree.command()
async def viewer(interaction: Interaction, viewer: User, project_name: str):
    if interaction.user == viewer:
        await interaction.response.send_message(f'{interaction.user.mention}, 自分に権限を与える必要はありません。')
        return

    try:
        addViewer(interaction.user, viewer, project_name)
    except NoProjectError:
        await interaction.response.send_message(f'{interaction.user.mention}, {viewer.mention} のプロジェクトに {project_name} はありません。')
    except AddedError:
        await interaction.response.send_message(f'{interaction.user.mention}, {viewer.mention} の {project_name} の閲覧権限は既に持っています。')
    await interaction.response.send_message(f'{interaction.user.mention}, {viewer.mention}に {project_name} の閲覧権限を与えました。')


# @client.tree.command()
# async def others_project(interaction: Interaction):
#     try:
#         project = getOthersProject(interaction)

# 開始できるプロジェクトの自動入力
@start.autocomplete('project')
async def start_project_autoconplete(
    interaction: Interaction,
    current: str,
) -> list[Choice[str]]:
    user_projects = getUserNotWorkingProjects(interaction.user)
    user_projects_name = [p["name"]for p in user_projects]
    return [
        Choice(name=project, value=project) for project in user_projects_name if current.lower() in project.lower()
    ]


# 終了できるプロジェクトの自動入力(TODO:選択肢以外の選択拒否)
@stop.autocomplete('project')
async def stop_project_autoconplete(
    interaction: Interaction,
    current: str,
) -> list[Choice[str]]:
    user_projects = getUserWorkingProjects(interaction.user)
    user_projects_name = [p["name"]for p in user_projects]
    return [
        Choice(name=project, value=project) for project in user_projects_name if current.lower() in project.lower()
    ]


# 全プロジェクトの自動入力(TODO:選択肢以外の選択拒否)
@project_detail.autocomplete('project_name')
async def project_detail_autoconplete(
    interaction: Interaction,
    current: str,
) -> list[Choice[str]]:
    user_projects = getUserProjects(interaction.user)
    user_projects_name = [p["name"]for p in user_projects]
    return [
        Choice(name=project, value=project) for project in user_projects_name if current.lower() in project.lower()
    ]


@client.tree.command()
async def hello(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')

client.run(os.getenv("TOKEN"))
