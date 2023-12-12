from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db import Base, session
from review import Review

class Restaurant(Base):


    def reviews(self):
        return self.reviews

    def customers(self):
        if not self.reviews:
            return "No customers have reviewed this restaurant."
        return [review.customer() for review in self.reviews]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        review_strings = []
        for review in self.reviews:
            review_string = (f"Review for {self.name} by {review.customer().full_name()}: {review.star_rating} stars.")
            review_strings.append(review_string)
        return review_strings
