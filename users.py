from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    submissions = relationship("Submission", back_populates="user")
    suggestions = relationship("Suggestion", back_populates="user")

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.username)


Base.metadata.create_all(engine)
