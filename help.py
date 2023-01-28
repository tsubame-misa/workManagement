command_detail_dict = {
    "start": {
        "name": "`/start <project_name> <description>`",
        "value": '指定したプロジェクトの作業の開始。descriptionに作業内容を指定することもできる。\n'
        + ' <返り値> 開始時刻 xx:xx:xx\n'
        + ' <備考> 初めて入力されるプロジェクト名の場合は自動的にプロジェクトが作成されます。'
    },
    "stop": {
        "name": "`/stop <project_name>`",
        "value": '指定したプロジェクトの作業の終了。\n'
        + ' <返り値>\n'
        + ' 終了時刻 xx:xx:xx\n'
        + ' 今回の作業時間 xx:xx:xx\n'
        + ' 合計作業時間 xx:xx:xx\n'
    },
    "projects": {
        "name": "`/projects`",
        "value": "プロジェクトの一覧表示\n"
        + '各プロジェクトの累計作業時間を確認できます。\n'
        + ' <返り値> '
        + '<project_name_n>：合計作業時間\n'
        + '<project_name_n+1>：合計作業時間 作業中\n'
    },
    "project_detail": {
        "name": "`/project_detail`",
        "value": "任意のプロジェクトの作業時間の詳細表示\n"
        + ' <返り値> '
        + '【<project_name_n>】\n'
        + ' 詳細なし : xx:xx:xx\n'
        + ' <description_n> : xx:xx:xx\n'
        + ' <description_n+1> : xx:xx:xx\n'
        + ' 合計作業時間: xx:xx:xx\n'
    },
    "viewer": {
        "name": "`/viewer`",
        "value": "<viewer>に自分のプロジェクト<project_name>の閲覧権限を付与。\n"
    },
    "others_projects": {
        "name": "`/others_projects`",
        "value": "閲覧権限を持つ他者のプロジェクトの作業時間の表示\n"
        + ' <返り値> '
        + '【<user_id> :<project_name_n>】\n'
        + ' 詳細なし : xx:xx:xx\n'
        + ' <description_n> : xx:xx:xx\n'
        + ' <description_n+1> : xx:xx:xx\n'
        + ' 合計作業時間: xx:xx:xx\n'
    },
    "download_file": {
        "name": "`/download_file`",
        "value": "プロジェクトの詳細データ(json)のダウンロード\n"
        + '各プロジェクトの累計作業時間と作業時間・内容の詳細が記載されたjsonファイルをダウンロードします。\n'
    }
}


def getCommandDetail(command):
    return command_detail_dict[command]
