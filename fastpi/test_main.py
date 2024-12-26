# from fastapi.testclient import TestClient
# from main import app
# from utils import get_db
# from db.databaseConnect import Base
# from sqlalchemy import create_engine, StaticPool
# from sqlalchemy.orm import sessionmaker


# client = TestClient(app)

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}, poolclass=StaticPool)
# Test_Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def override_get_db():
#     db = Test_Session_Local()
#     yield db
#     db.close()


# def setup():
#     Base.metadata.create_all(bind=engine)

# # def tear_down():
# #     Base.metadata.drop_all(bind=engine)

# app.dependency_overrides[get_db] = override_get_db

# def test_start():
#     response  = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == "Server is running"


# def test_create_user():
#     response = client.post("/register", json={
#         "name":"Gideon",
#         "email":"gideon@gmail.com",
#         "password":"giiid"
#     })
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["name"]  == "Gideon"

#     # assert response.json() == {
#     #     "name":"Gideon",
#     #     "email":"giideon@gmail.com",
#     #     "password":"$2b$12$pDcXLEu/9nNrBHb1M6omgeno0/oxdHDxXT0vnEZyB5c2F6/4AyqrC"
#     # }



from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from db.databaseConnect import Base
from utils import get_db

# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to override the get_db dependency in the utils app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

def setup():
    Base.metadata.create_all(bind=engine)

def tear_down():
    Base.metadata.drop_all(bind=engine)
    
app.dependency_overrides[get_db] = override_get_db


def test_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running"


def test_register():
    response = client.post("/register", json={
        "name":"Gideon",
        "email":"gideon@gmail.com",
        "password":"giiid"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Gideon"