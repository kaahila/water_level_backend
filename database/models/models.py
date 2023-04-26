from sqlalchemy import Float, Column, BigInteger, TIMESTAMP,Integer

from database import Base


class LF7(Base):
    __tablename__ = "lf7"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_on = Column(Integer, index=True)
    value = Column(Float)
