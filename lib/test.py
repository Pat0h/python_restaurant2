from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Restaurant, Customer, Review, Base

# Establish a connection to the database
engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Test your methods here using SQLAlchemy queries and relationships
# For example:
first_customer = session.query(Customer).first()
print("Customer's full name:", first_customer.full_name())
print("Customer's favorite restaurant:", first_customer.favorite_restaurant())

# Test adding a review for a restaurant by a customer
restaurant_to_review = session.query(Restaurant).filter_by(name="Sample Restaurant").first()
if restaurant_to_review:
    first_customer.add_review(restaurant_to_review, 4)
    session.commit()
    print("Added review for the restaurant by the customer")

# Test getting all reviews for a restaurant
restaurant_reviews = restaurant_to_review.all_reviews()
if restaurant_reviews:
    print("All reviews for the restaurant:")
    for review in restaurant_reviews:
        print(review.full_review())

# Test deleting all reviews for a restaurant by a customer
if restaurant_to_review:
    first_customer.delete_reviews(restaurant_to_review)
    session.commit()
    print("Deleted all reviews for the restaurant by the customer")

# Test relationships
first_review = session.query(Review).first()
print("Review's customer:", first_review.customer().full_name())
print("Review's restaurant:", first_review.restaurant().name)


