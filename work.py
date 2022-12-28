import datetime
import time
from error import NoProjectError, NoUserError, NoStartError

"""
データ形式
TODO:データベース化
users = [user:{
    project1: {
        start_time,
        total_time,
    }
    project2: {
        start_time,
        total_time,
    }
}, ]
"""
users = {}


def getDate():
    date = datetime.datetime.now()
    return date


def formatDate(date):
    return date.strftime('%Y/%m/%d %H:%M:%S')


def elapsed_time_str(seconds):
    """秒をhh:mm:ss形式の文字列で返す

    Parameters
    ----------
    seconds : float
        表示する秒数

    Returns
    -------
    str
        hh:mm:ss形式の文字列
    """
    seconds = int(seconds + 0.5)    # 秒数を四捨五入
    h = seconds // 3600             # 時の取得
    m = (seconds - h * 3600) // 60  # 分の取得
    s = seconds - h * 3600 - m * 60  # 秒の取得

    return f"{h:02}:{m:02}:{s:02}"  # hh:mm:ss形式の文字列で返す


def initUser(user):
    global users
    users[user] = {}


def addProject(user, project):
    global users
    init_time = {
        "start_time": None,
        "total_time": datetime.timedelta(seconds=0)
    }
    users[user][project] = init_time


def startWork(user, project):
    global users
    my_start_time = getDate()
    if not user in users:
        initUser(user)
    if not project in users[user]:
        addProject(user, project)
    users[user][project]["start_time"] = my_start_time
    return my_start_time


def stopWork(user, project):
    global users
    # NOTE:分ける必要なかった
    if not user in users or not project in users[user] or users[user][project]["start_time"] is None:
        raise NoStartError
    end_time = getDate()
    work_time = end_time-users[user][project]["start_time"]
    users[user][project]["total_time"] += work_time
    users[user][project]["start_time"] = None
    return {"end_time": end_time, "work_time":  elapsed_time_str(work_time.total_seconds()), "total_time": elapsed_time_str(users[user][project]["total_time"].total_seconds())}


def getUserProject(user):
    if not user in users:
        raise NoUserError
    projects = []
    for key in users[user]:
        project = f'{key} : 合計作業時間 {elapsed_time_str(users[user][key]["total_time"].total_seconds())}'
        projects.append(project)
    str_project = '\n'.join(projects)

    return str_project


# startWork("hoge", "patakara")
# time.sleep(3)
# print(stopWork("hoge", "patakara"))
# startWork("hoge", "sum")
# time.sleep(3)
# print(stopWork("hoge", "patakara"))
# print(getUserProject("hoge"))
