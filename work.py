from error import NoStartError, WorkingError, NoFinishedError, NoProjectError, AddedError
from common import elapsed_time_str, getDate, getWorkingTime
from api import getUserProjects, updateWork, insertWork, insertProject, getUserWorkingWork, updateProject, getUserProjectWorks, addRoll, getRoll, getOthersProjectRoll, getProjectFromId
from discord import User


def getNames(user_projects):
    project_ids = []
    for data in user_projects:
        project = f'{data["name"]}'
        project_ids.append(project)
    return project_ids


def getProjectByName(project_name, user_projects):
    for project in user_projects:
        if project["name"] == project_name:
            return project
    return None


def getUserProject(user, project_name):
    user_projects = getUserProjects(user)

    if not project_name in getNames(user_projects):
        return None

    project = getProjectByName(project_name, user_projects)
    return project


def startWork(user, project_name, description):
    my_start_time = getDate()

    project = getUserProject(user, project_name)
    if project is None:
        p_obj = {
            "user_id": str(user),
            "name": project_name,
            "working": True
        }
        project = insertProject(p_obj)
    elif project["working"]:
        raise WorkingError
    else:
        updateProject(project["id"], project["total_seconds"], True)

    # 正常に動いていたらいらないはず
    work = getUserWorkingWork(project["id"])
    if not work is None and len(work) > 1:
        raise NoFinishedError

    work_obg = {"project_id": project["id"],
                "start_time": my_start_time, "description": description}
    insertWork(work_obg)

    return my_start_time


def stopWork(user, project_name):
    project = getUserProject(user, project_name)
    if project is None or project["working"] is False:
        raise NoStartError

    work = getUserWorkingWork(project["id"])
    if len(work) > 1:
        raise NoFinishedError
    else:
        work = work[0]

    end_time = getDate()
    work_time = getWorkingTime(work["start_time"], end_time)

    project["total_seconds"] += work_time
    work["end_time"] = str(end_time)

    updateProject(project["id"], project["total_seconds"], False)

    updateWork(work["id"], work["end_time"])

    return {"end_time": end_time, "work_time":  elapsed_time_str(work_time), "total_time": elapsed_time_str(project["total_seconds"]), "description": work["description"]}


def getUserProjectsText(user):
    user_projects = getUserProjects(user)
    projects = []
    for project in user_projects:
        text = f'{project["name"]}: 合計作業時間 {elapsed_time_str(project["total_seconds"])}'
        if project["working"]:
            text += f' 作業中'
        projects.append(text)

    projects_text = '\n'.join(projects)
    return projects_text


def getUserProjectDetailText(user, project_name):
    detail_text = []

    project = getUserProject(user, project_name)

    if project is None:
        return None

    text = f'【{project["name"]}】'
    detail_text.append(text)

    project_detail_list = getUserProjectDetail(project["id"])
    for k, v in project_detail_list.items():
        text = f' {k} : {elapsed_time_str(v)}'
        detail_text.append(text)

    text = f'合計作業時間 : {elapsed_time_str(project["total_seconds"])}'
    detail_text.append(text)

    joined_text = '\n'.join(detail_text)
    return joined_text


def getProjectDetailText(project, others=False):
    detail_text = []
    if others:
        text = f'【{project["user_id"]} {project["name"]}】'
    else:
        text = f'【{project["name"]}】'
    detail_text.append(text)

    project_detail_list = getUserProjectDetail(project["id"])
    for k, v in project_detail_list.items():
        text = f' {k} : {elapsed_time_str(v)}'
        detail_text.append(text)

    text = f'合計作業時間 : {elapsed_time_str(project["total_seconds"])}'
    detail_text.append(text)

    joined_text = '\n'.join(detail_text)
    return joined_text


def getUserProjectDetail(project_id):
    works = getUserProjectWorks(project_id)
    description_dict = {"詳細なし": 0}
    for work in works:
        time = getWorkingTime(work["start_time"], work["end_time"])
        if work["description"] is None:
            description_dict["詳細なし"] += time
        elif work["description"] in description_dict:
            description_dict[work["description"]] += time
        else:
            description_dict[work["description"]] = time

    return description_dict


def addViewer(user_id, viewer_id, project_name):
    project = getUserProject(user_id, project_name)

    if project is None:
        raise NoProjectError

    roll = getRoll(viewer_id, project["id"])
    if roll is None:
        addRoll(viewer_id, project["id"])
    else:
        raise AddedError


def getOthersProject(viewer_id):
    roll = getOthersProjectRoll(viewer_id)
    project_ids = [r["project_id"] for r in roll]

    print(project_ids)

    if len(project_ids) == 0:
        return None

    project_text = []
    for id in project_ids:
        p = getProjectFromId(id)
        text = getProjectDetailText(p, True)
        project_text.append(text)

    joined_text = '\n\n'.join(project_text)
    return joined_text
