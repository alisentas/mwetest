from sqlalchemy import Column, Integer, String

from database import Base, engine


class Mwe(Base):
    __tablename__ = 'mwes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    meaning = Column(String)

    def __repr__(self):
        return "<MWE(id='%s', name='%s')>" % (self.id, self.name)


Base.metadata.create_all(engine)
