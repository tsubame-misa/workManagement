from sqlalchemy.ext.automap import automap_base
from db import engine

Base = automap_base()


class Projects(Base):
    __tablename__ = 'projects'

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'total_seconds': self.total_seconds,
            'working': self.working,
        }


class Works(Base):
    __tablename__ = 'works'

    def to_json(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'description': self.description,
        }


Base.prepare(engine, reflect=True)
