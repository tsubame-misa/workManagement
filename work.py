from error import NoStartError, WorkingError, NoFinishedError
from common import elapsed_time_str, getDate
from api import getUserProjects, updateWork, insertWork, insertProject, getUserWorkingWork, updateProject


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
    start_time = work["start_time"]
    work_time = end_time-start_time

    project["total_seconds"] += int(work_time.total_seconds())
    work["end_time"] = str(end_time)

    updateProject(project["id"], project["total_seconds"], False)

    updateWork(work["id"], work["end_time"])

    return {"end_time": end_time, "work_time":  elapsed_time_str(work_time.total_seconds()), "total_time": elapsed_time_str(project["total_seconds"]), "description": work["description"]}


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
