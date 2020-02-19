from enum import auto, Enum

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine

POSITIVE_REVIEW = 1
NEGATIVE_REVIEW = 0
NEUTRAL_REVIEW = 2


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    review_type = Column(Integer)

    mwe_id = Column(Integer, ForeignKey('mwes.id'))
    mwe = relationship("Mwe", back_populates="reviews")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="reviews")

    submission_id = Column(Integer, ForeignKey('submissions.id'))
    submission = relationship("Submission", back_populates="reviews")

    def __repr__(self):
        return "<Review(id='%s', type='%d')>" % (self.id, self.review_type)


Base.metadata.create_all(engine)
