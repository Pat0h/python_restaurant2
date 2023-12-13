from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    def reviews(self):
        return [review for review in Review.query.filter_by(restaurant_id=self.id)]

    def customers(self):
        return [review.customer() for review in self.reviews()]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [
            f"Review for {self.name} by {review.customer().full_name()}: {review.star_rating} stars."
            for review in self.reviews()
        ]

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    def reviews(self):
        return [review for review in Review.query.filter_by(customer_id=self.id)]

    def restaurants(self):
        return [review.restaurant() for review in self.reviews()]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        reviews = self.reviews()
        if reviews:
            return max(reviews, key=lambda x: x.star_rating).restaurant()

    def add_review(self, restaurant, rating):
        new_review = Review(customer_id=self.id, restaurant_id=restaurant.id, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews = Review.query.filter_by(customer_id=self.id, restaurant_id=restaurant.id).all()
        for review in reviews:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    star_rating = Column(Integer)

    def customer(self):
        return session.query(Customer).get(self.customer_id)

    def restaurant(self):
        return session.query(Restaurant).get(self.restaurant_id)

    def full_review(self):
        return f"Review for {self.restaurant().name} by {self.customer().full_name()}: {self.star_rating} stars."

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
