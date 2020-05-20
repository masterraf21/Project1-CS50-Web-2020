from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def load_data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1,
                      converters={0: lambda s: str(s)})
    return data.tolist()


class Books(Base):
    __tablename__ = 'Books'
    # Table columns
    isbn = Column(Varchar(10), primary_key=True, nullable=False)
    title = Column(Varchar(50))
    author = Column(Varchar(50))
    year = Column(Integer)


if __name__ == "__main__":
    t = time()
    connect_db()
    # Load file from csv
    file_name = "books.csv"
    data = load_data(file_name)
    try:
        for i in data:
            record = Books(**{
                'isbn': id[0],
                'title': id[1],
                'author': id[2],
                'year': id[3]
            })
            db.add(record)
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()

    print("Time elapsed: {} s".format(str(time()-t)))
