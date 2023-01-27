import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()


def create_engine():
    drivername = 'postgresql+pg8000'
    db_host = os.getenv('PGHOST')
    db_port = os.getenv('PGPORT')
    db_name = os.getenv('PGDATABASE')
    db_user = os.getenv('PGUSER')
    db_pass = os.getenv('PGPASSWORD')
    target = os.environ.get('TARGET', 'development')

    if target == 'production':
        cloud_sql_connection_name = os.environ.get('CONNECTION')
        socket_path = '/cloudsql/{}/.s.PGSQL.5432'.format(
            cloud_sql_connection_name)
        return sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername=drivername,
                username=db_user,
                password=db_pass,
                database=db_name,
                query={
                    'unix_sock': socket_path
                }
            ),
        )

    return sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername=drivername,
            username=db_user,
            password=db_pass,
            database=db_name,
            host=db_host,
            port=db_port,
        ),
    )


engine = create_engine()
Session = sessionmaker(bind=engine)


def create_session():
    return Session()
