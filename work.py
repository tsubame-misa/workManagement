import datetime
from error import NoStartError
from common import elapsed_time_str, getDate
from api import getUserProject, updateWork, insertWork


def startWork(user, project_name):
    my_start_time = getDate()

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

    return {"end_time": end_time, "work_time":  elapsed_time_str(work_time.total_seconds()), "total_time": elapsed_time_str(project["total_time"])}
