from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship

from database import Base, engine, session


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    category = Column(String)
    language = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="submissions")

    mwe_id = Column(Integer, ForeignKey("mwes.id"))
    mwe = relationship("Mwe", back_populates="submissions")

    reviews = relationship("Review", back_populates="submission")

    @hybrid_property
    def review_count(self):
        return len(self.reviews)

    def __repr__(self):
        return "<Value(id='%s', value='%s')>" % (self.id, self.value)


Base.metadata.create_all(engine)
