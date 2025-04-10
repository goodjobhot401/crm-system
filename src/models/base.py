from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def as_dict(self):
        return {columns.name: getattr(self, columns.name) for columns in self.__table__.columns}
