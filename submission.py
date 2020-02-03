from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    category = Column(String)
    points = Column(Integer)
    users_who_reviewed = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="submissions")

    def __repr__(self):
        return "<Value(id='%s', value='%s')>" % (self.id, self.value)


Base.metadata.create_all(engine)
