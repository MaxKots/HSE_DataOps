import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mlsvc:mlsvc_pass@ml-service-db:5432/mlsvc",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_data = Column(Text, nullable=False)
    output = Column(Float, nullable=False)
    model_version = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)


def log_prediction(input_data: str, output: float, model_version: str):
    session = SessionLocal()
    try:
        entry = PredictionLog(
            input_data=input_data,
            output=output,
            model_version=model_version,
        )
        session.add(entry)
        session.commit()
    finally:
        session.close()