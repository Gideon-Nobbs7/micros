from db.databaseConnect import sessionLocal


def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()
