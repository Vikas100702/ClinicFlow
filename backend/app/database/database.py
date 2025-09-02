from lib.lib_import import os, create_engine, declarative_base, sessionmaker, load_dotenv
load_dotenv()

db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autoflush = False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()