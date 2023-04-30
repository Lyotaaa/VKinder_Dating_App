from configparser import ConfigParser
import sqlalchemy
from models import create_tables


def get_DSN(file_name):
    config = ConfigParser()
    config.read(file_name)
    return config['DB_info']['DSN']


if __name__ == '__main__':
    DSN = get_DSN('config.ini')
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)
