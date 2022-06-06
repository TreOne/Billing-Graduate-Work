from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, Session
from auth_api.settings.settings import Settings

settings = Settings()

metadata = MetaData()
Base = declarative_base(metadata=metadata)

engine = create_engine(settings.alchemy.database_uri)
session = Session(engine)
