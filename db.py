import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker


def create_engine():
    drivername = 'postgresql+pg8000'
    db_host = os.environ.get('PGHOST')
    db_port = os.environ.get('PGPORT')
    db_name = os.environ.get('PGDATABASE')
    db_user = os.environ.get('PGUSER')
    db_pass = os.environ.get('PGPASSWORD')
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
