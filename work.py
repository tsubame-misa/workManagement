import datetime
import time
from error import NoStartError
from common import elapsed_time_str
from api import getUserProject, updateWork, insertWork

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


def startWork(user, project_name):
    # global users
    my_start_time = getDate()

    # if not user in users:
    #     initUser(user)
    # if not project in users[user]:
    #     addProject(user, project)
    # users[user][project]["start_time"] = my_start_time
    project = getUserProject(user, project_name)
    if project is None:
        obj = {
            "user_id": str(user),
            "project_name": project_name,
            "start_time": str(my_start_time),
            "total_time": 0,
        }
        insertWork(obj)
    else:
        updateWork(user, project_name, str(
            my_start_time), project["total_time"])

    return my_start_time


def stopWork(user, project_name):
    # global users
    # # NOTE:分ける必要なかった
    # if not user in users or not project in users[user] or users[user][project]["start_time"] is None:
    #     raise NoStartError
    project = getUserProject(user, project_name)
    if project is None:
        raise NoStartError
    end_time = getDate()
    start_time = datetime.datetime.strptime(
        project["start_time"], '%Y-%m-%dT%H:%M:%S.%f')
    work_time = end_time-start_time
    project["total_time"] += int(work_time.total_seconds())
    project["start_time"] = None
    updateWork(user, project_name, None, project["total_time"])
    # users[user][project]["total_time"] += work_time
    # users[user][project]["start_time"] = None
    return {"end_time": end_time, "work_time":  elapsed_time_str(work_time.total_seconds()), "total_time": elapsed_time_str(project["total_time"])}


# def getUserProject(user):
#     if not user in users:
#         raise NoUserError
#     projects = []
#     for key in users[user]:
#         project = f'{key} : 合計作業時間 {elapsed_time_str(users[user][key]["total_time"].total_seconds())}'
#         projects.append(project)
#     str_project = '\n'.join(projects)

#     return str_project


# startWork("hoge", "patakara")
# time.sleep(3)
# print(stopWork("hoge", "patakara"))
# startWork("hoge", "sum")
# time.sleep(3)
# print(stopWork("hoge", "patakara"))
# print(getUserProject("hoge"))
