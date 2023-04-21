import sqlalchemy
from models import create_tables


if __name__ == '__main__':
    DSN = 'postgresql://postgres:6996@localhost:5432/SQLAlchemy'
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)
