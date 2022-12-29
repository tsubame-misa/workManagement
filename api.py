import requests
import os
import json
from common import elapsed_time_str, formatDate
from error import ApiError
import datetime


# def getUsers():
#     url = 'https://tsubame.hasura.app/api/rest/work_management/user'
#     headers = {
#         "Content-Type": "application/json",
#         "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
#     }

#     res = requests.get(url, headers=headers)
#     data = res.json()

#     if "error" in data:
#         raise ApiError

#     users = []
#     for data in data["work"]:
#         users.append(data["user_id"])

#     return users


# def getUserProjects(user):
#     url = "https://tsubame.hasura.app/api/rest/work_management/user/projects"
#     headers = {
#         "Content-Type": "application/json",
#         "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
#     }
#     data = json.dumps({"id": str(user)})
#     res = requests.post(url, headers=headers, data=data)
#     data = res.json()

#     if "error" in data:
#         print(data)
#         raise ApiError

#     projects = []
#     for data in data["work"]:
#         project = f'{data["project_name"]} : 合計作業時間 {elapsed_time_str(data["total_time"])}'
#         if not data["start_time"] is None:
#             start_time = datetime.datetime.strptime(
#                 data["start_time"], '%Y-%m-%dT%H:%M:%S')
#             project += f'  作業中（{formatDate(start_time)}から）'
#         projects.append(project)
#     str_project = '\n'.join(projects)

#     return str_project


# def getUserProject(user, project):
#     url = "https://tsubame.hasura.app/api/rest/work_management/user/project"
#     headers = {
#         "Content-Type": "application/json",
#         "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
#     }
#     data = json.dumps({"user_id": str(user), "project_name": project})
#     res = requests.post(url, headers=headers, data=data)
#     data = res.json()

#     if "error" in data:
#         raise ApiError

#     if len(data["work"]) == 0:
#         print(data)
#         return None

#     return({"start_time": data["work"][0]["start_time"],
#             "total_time": data["work"][0]["total_time"]})


# def insertWork(data):
#     url = "https://tsubame.hasura.app/api/rest/work_management/insert/work"
#     headers = {
#         "Content-Type": "application/json",
#         "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
#     }
#     data = json.dumps({"object": data})
#     res = requests.post(url, headers=headers, data=data)
#     data = res.json()
#     if "error" in data:
#         print(data)
#         raise ApiError


# def updateWork(user, project_name, start_time, total_time):
#     url = "https://tsubame.hasura.app/api/rest/update/project"
#     headers = {
#         "Content-Type": "application/json",
#         "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
#     }
#     data = json.dumps({"user_id": str(user), "project_name": project_name,
#                       "start_time": start_time, "total_time": total_time})
#     res = requests.put(url, headers=headers, data=data)
#     data = res.json()
#     if "error" in data:
#         print(data)
#         raise ApiError


# def getUsers():
#     url = 'https://tsubame.hasura.app/api/rest/work_management/users'
#     headers = {
#         "Content-Type": "application/json",
#         "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
#     }

#     res = requests.get(url, headers=headers)
#     data = res.json()

#     if "error" in data:
#         raise ApiError

#     users = []
#     for data in data["users"]:
#         users.append(data["id"])

#     return users


def getUserProjects(user):
    url = "https://tsubame.hasura.app/api/rest/work_management/user/projects"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"user_id": str(user)})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()

    if "error" in data:
        print(data)
        raise ApiError

    projects = []
    for data in data["projects"]:
        # project = f'{data["project_name"]} : 合計作業時間 {elapsed_time_str(data["total_time"])}'
        project = f'{data["name"]}'
        # if not data["start_time"] is None:
        #     start_time = datetime.datetime.strptime(
        #         data["start_time"], '%Y-%m-%dT%H:%M:%S')
        #     project += f'  作業中（{formatDate(start_time)}から）'
        projects.append(project)
    str_project = '\n'.join(projects)

    return str_project


def getUserWorkingProject(project_id):
    url = "https://tsubame.hasura.app/api/rest/work_management/user/working/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"project_id": project_id})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()

    if "error" in data:
        raise ApiError

    if len(data["works"]) == 0:
        print(data)
        return None

    return({"start_time": data["works"][0]["start_time"],
            "end_time": data["works"][0]["end_time"]})


def insertProject(user, project_name):
    url = "https://tsubame.hasura.app/api/rest/work_management/insert/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    # TODO: make
    data = {"user_id": user, "name": project_name}
    data = json.dumps({"object": data})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError
    return data["insert_projects_one"]["id"]


def updateProject(id, total_seconds, working):
    url = "https://tsubame.hasura.app/api/rest/work_management/update/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps(
        {"id": id, "total_seconds": total_seconds, "working": working})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError
    return data["insert_projects_one"]["id"]


def insertWork(data):
    url = "https://tsubame.hasura.app/api/rest/work_management/insert/work"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    # TODO: make
    data = {"project_id": 1, "start_time": "2022-12-29 22:20:11"}
    data = json.dumps({"object": data})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError
    return data["insert_works_one"]["id"]


def updateWork(work_id):
    url = "https://tsubame.hasura.app/api/rest/update/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"id": 4, "end_time": "2022-12-29 22:26:27"})
    res = requests.put(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError
    return data["update_works_by_pk"]
