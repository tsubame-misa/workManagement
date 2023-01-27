from sqlalchemy.ext.automap import automap_base
from db import engine
import json

Base = automap_base()


class Projects(Base):
    __tablename__ = 'projects'

    def load_json(self, data):
        if data is None:
            return None
        return json.loads(data)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'total_seconds': self.total_seconds,
            'working': self.working
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


class Rolls(Base):
    __tablename__ = "rolls"

    def to_json(self):
        return {
            'user_id': self.user_id,
            'project_id': self.project_id,
            'roll': self.roll,
        }


Base.prepare(engine, reflect=True)
