command_detail_dict = {
    "start": {
        "name": "`\start <project_name> <description>`",
        "value": '指定したプロジェクトの作業の開始。descriptionに作業内容を指定することもできる。\n'
        + ' <返り値> 開始時刻 xx:xx:xx\n'
        + ' <備考> 初めて入力されるプロジェクト名の場合は自動的にプロジェクトが作成されます。'
    },
    "stop": {
        "name": "`\stop <project_name>`",
        "value": '指定したプロジェクトの作業の終了。\n'
        + ' <返り値>終了時刻 xx:xx:xx, 今回の作業時間 xx:xx:xx, 合計作業時間 xx:xx:xx\n'
    },
    "projects": {
        "name": "`\projects`",
        "value": "プロジェクトの一覧表示\n"
        + '各プロジェクトの累計作業時間を確認できます。\n'
        + ' <返り値> '
        + 'プロジェクト名n：合計作業時間\n'
        + 'プロジェクト名n+1：合計作業時間 作業中\n'
    },
    "download_file": {
        "name": "`\download_file`",
        "value": "プロジェクトの詳細データ(json)のダウンロード\n"
        + '各プロジェクトの累計作業時間と作業時間・内容の詳細が記載されたjsonファイルをダウンロードします。\n'
    }
}


def getCommandDetail(command):
    return command_detail_dict[command]
