from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, session
from customer import Customer
from restaurant import Restaurant


class Review(Base):

    def customer(self):
        return session.query(Customer).filter_by(id=self.customer_id).first()

    def restaurant(self):
        return session.query(Restaurant).filter_by(id=self.restaurant_id).first()

    def full_review(self):
        return f"Review for {self.restaurant().name} by {self.customer().full_name()}: {self.star_rating} stars."
