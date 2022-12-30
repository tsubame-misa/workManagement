def getHelpText():
    msg = '\n各ユーザーがプロジェクトごとに勤怠をつけることができるbotです。\n\n'\
        '-----------------------------------------------------------\n\n'\
        '【プロジェクトの開始】\n'\
        ' コマンド：\start プロジェクト名\n'\
        ' 返り値　：開始時刻 xx:xx:xx\n'\
        ' 備考　　：初めて入力されるプロジェクト名の場合は自動的にプロジェクトが作成されます。\n\n'\
        '【プロジェクトの終了】\n'\
        ' コマンド：\stop プロジェクト名\n'\
        ' 返り値　：終了時刻 xx:xx:xx, 今回の作業時間 xx:xx:xx, 合計作業時間 xx:xx:xx\n\n'\
        '【プロジェクトの一覧表示】\n'\
        ' コマンド：\projects \n'\
        ' 返り値　：プロジェクト名n：合計作業時間\n'\
        ' 　　　　　プロジェクト名n+1：合計作業時間 作業中\n'
    return msg


command_detail_dict = {
    "start": {
        "name": "`\start <project_name> <description>`",
        "value": '指定したプロジェクトの作業の開始。descriptionに作業内容を指定することもできる。\n'
        + ' 返り値　：開始時刻 xx:xx:xx\n'
        + ' 備考　　：初めて入力されるプロジェクト名の場合は自動的にプロジェクトが作成されます。'
    },
    "stop": {
        "name": "`\stop <project_name>`",
        "value": '指定したプロジェクトの作業の終了。\n'
        + ' 返り値：終了時刻 xx:xx:xx, 今回の作業時間 xx:xx:xx, 合計作業時間 xx:xx:xx\n'
        + ' 備考　：初めて入力されるプロジェクト名の場合は自動的にプロジェクトが作成されます。'
    },
    "projects": {
        "name": "`\projects`",
        "value": "プロジェクトの一覧表示\n"
        + '各プロジェクトの累計作業時間を確認できます。\n'
        + ' 返り値　：プロジェクト名n：合計作業時間\n'
        + ' 　　　　　プロジェクト名n+1：合計作業時間 作業中\n'
    },
    "download_file": {
        "name": "`\download_file`",
        "value": "プロジェクトの詳細データ(json)のダウンロード\n"
        + '各プロジェクトの累計作業時間と作業時間・内容の詳細が記載されたjsonファイルをダウンロードします。\n'
    }
}

select_command_data = [{
    type: "STRING",
    "name": "コマンド",
    "description": "コマンドを選択して下さい",
    "required": False,
    "choices": [
        {"name": "start", "value": "start"},
        {"name": "stop", "value": "stop"},
        {"name": "projects", "value": "projects"},
        {"name": "download_file", "value": "download_file"},
    ]
}],


def getCommandDetail(command):
    return command_detail_dict[command]
