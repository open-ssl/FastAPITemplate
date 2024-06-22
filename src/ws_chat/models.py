from src.database import DeclarativeBase
from sqlalchemy import Integer, String, Column


class Messages(DeclarativeBase):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.__columns__}
