from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "mysql+pymysql://nUnaTjPe8coZWEc.root:jglbTlz4ahI8NjCz@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/test?ssl_ca=C:/Users/nijus/Downloads/isrgrootx1.pem"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl":{
           "ssl" :True
        }
    }
)

Sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()