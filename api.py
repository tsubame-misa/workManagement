import requests
import os
import json
from common import elapsed_time_str
from error import ApiError


def getUsers():
    url = 'https://tsubame.hasura.app/api/rest/work_management/user'
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    if "error" in data:
        raise ApiError

    users = []
    for data in data["work"]:
        users.append(data["user_id"])

    return users


def getUserProjects(user):
    url = "https://tsubame.hasura.app/api/rest/work_management/user/projects"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"id": str(user)})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()

    if "error" in data:
        print(data)
        raise ApiError

    projects = []
    for data in data["work"]:
        project = f'{data["project_name"]} : 合計作業時間 {elapsed_time_str(data["total_time"])}'
        projects.append(project)
    str_project = '\n'.join(projects)

    return str_project


def getUserProject(user, project):
    url = "https://tsubame.hasura.app/api/rest/work_management/user/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"user_id": str(user), "project_name": project})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()

    if "error" in data:
        raise ApiError

    if len(data["work"]) == 0:
        print(data)
        return None

    return({"start_time": data["work"][0]["start_time"],
            "total_time": data["work"][0]["total_time"]})


def insertWork(data):
    url = "https://tsubame.hasura.app/api/rest/work_management/insert/work"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"object": data})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError


def updateWork(user, project_name, start_time, total_time):
    url = "https://tsubame.hasura.app/api/rest/update/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"user_id": str(user), "project_name": project_name,
                      "start_time": start_time, "total_time": total_time})
    res = requests.put(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError
