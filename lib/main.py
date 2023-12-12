from db import session
from customer import Customer
from restaurant import Restaurant
from review import Review

# Test your methods here
first_customer = session.query(Customer).first()
print(first_customer.restaurants())

first_review = session.query(Review).first()
print(first_review.customer().full_name())

# ... and so on for other methods
