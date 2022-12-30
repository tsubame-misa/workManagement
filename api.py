import requests
import os
import json
from error import ApiError


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

    return data["projects"]


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
        return None

    return data["works"]


def insertProject(data):
    url = "https://tsubame.hasura.app/api/rest/work_management/insert/project"
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
    return data["insert_projects_one"]


def updateProject(id, total_seconds, working):
    url = "https://tsubame.hasura.app/api/rest/work_management/update/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps(
        {"id": id, "total_seconds": total_seconds, "working": working})
    res = requests.put(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        print(data)
        raise ApiError
    return data["update_projects_by_pk"]


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
    return data["insert_works_one"]


def updateWork(work_id, end_time):
    url = "https://tsubame.hasura.app/api/rest/update/project"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"id": work_id, "end_time": end_time})
    res = requests.put(url, headers=headers, data=data)
    data = res.json()
    if "error" in data:
        raise ApiError
    return data["update_works_by_pk"]


def getUserProjectWorks(project_id):
    url = "https://tsubame.hasura.app/api/rest/work_management/users/projects/work"
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": os.getenv('HASURA_ADMIN_SECRET'),
    }
    data = json.dumps({"project_id": project_id})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()

    if "error" in data:
        print(data)
        raise ApiError

    return data["works"]
