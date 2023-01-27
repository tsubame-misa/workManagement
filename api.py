from models import Projects, Works
from db import create_session
from error import NoStartError


# ユーザーの持つプロジェクトを取得
def getUserProjects(user_id):
    session = create_session()
    works = session.query(Projects).filter_by(user_id=str(user_id)).all()
    works = [f.to_json() for f in works]
    session.close()
    return works


# 作業をしていないのプロジェクトを取得
def getUserNotWorkingProjects(user_id):
    session = create_session()
    works = session.query(Projects).filter_by(
        user_id=str(user_id), working=False).all()
    works = [f.to_json() for f in works]
    session.close()
    return works


# 作業中のプロジェクトを取得
def getUserWorkingProjects(user_id):
    session = create_session()
    works = session.query(Projects).filter_by(
        user_id=str(user_id), working=True).all()
    works = [f.to_json() for f in works]
    session.close()
    return works


# プロジェクトで作業中のワークを取得
def getUserWorkingWork(project_id):
    session = create_session()
    works = session.query(Works).filter_by(
        project_id=project_id, end_time=None).all()
    works = [f.to_json() for f in works]
    session.close()

    if len(works) == 0:
        return None

    return works


# プロジェクトのワークを取得
def getUserProjectWorks(project_id):
    session = create_session()
    works = session.query(Works).filter_by(
        project_id=project_id).all()
    works = [f.to_json() for f in works]
    session.close()

    return works


# 新しいプロジェクトの追加
def insertProject(obj):
    session = create_session()
    project = Projects(
        user_id=obj["user_id"],
        name=obj["name"],
        working=obj["working"]
    )
    session.add(project)
    session.commit()
    project = project.to_json()
    session.close()

    return project


# プロジェクトのアップデート（合計時間、作業中可否）
def updateProject(id, total_seconds, working):
    session = create_session()
    project_info = session.query(Projects).filter_by(
        id=id).first()

    if project_info is None:
        raise NoStartError

    project_info.total_seconds = total_seconds
    project_info.working = working
    session.commit()

    project_info = project_info.to_json()
    session.close()

    return project_info


# 新しいワークの追加
def insertWork(obj):
    session = create_session()
    work = Works(
        project_id=obj["project_id"],
        start_time=obj["start_time"],
        description=obj["description"]
    )
    session.add(work)
    session.commit()
    work = work.to_json()
    session.close()

    return work


# ワークのアップデート（終了時刻の追加）
def updateWork(id, end_time):
    session = create_session()
    work_info = session.query(Works).filter_by(
        id=id).first()

    if work_info is None:
        raise NoStartError

    work_info.end_time = end_time
    session.commit()

    work_info = work_info.to_json()
    session.close()

    return work_info
