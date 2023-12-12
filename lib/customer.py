from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, session
from restaurant import Restaurant
from review import Review

class Customer(Base):

    def reviews(self):
        return self.reviews

    def restaurants(self):
        if not self.reviews:
            return "This customer has not left any restaurant reviews."
        return [review.restaurant() for review in self.reviews]

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def favorite_restaurant(self):
        reviews = self.reviews()
        if not reviews:
            return "Customer has no reviews for any restaurant."
        highest_rating_review = max(reviews, key=lambda review: review.star_rating)
        return highest_rating_review.restaurant()

    def add_review(self, restaurant, rating):
        if isinstance(rating, int):
            review = Review(
                star_rating=rating,
                restaurant_id=restaurant.id,
                customer_id=self.id,
            )
            self.reviews.append(review)
            session.add(review)
            session.commit()
            return review
        else:
            return "Rating must be an integer."

    def delete_reviews(self, restaurant):
        reviewed_restaurants = self.restaurants()
        if restaurant in reviewed_restaurants:
            for res in reviewed_restaurants:
                if res.id == restaurant.id:
                    session.query(Review).filter_by(restaurant_id=res.id).delete()
                    session.commit()
            return "Restaurant review deleted successfully."
        else:
            return "Review not found."
