from database import Database
from datetime import date 

# Customer Class
class Customer:
  def __init__(self, db, name, email, password):
    self.db_connection = db
    self.name = name 
    self.email = email 
    self.password = password

  def add_to_db(self):
    query='INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)'
    self.db_connection.cursor.execute(query, (self.name, self.email, self.password))
    self.db_connection.db.commit()
    print(f'Added customers {self.name}, email : {self.email}, password: {self.password}')

  
  def get_customer_id(self):
    query='SELECT customer_id FROM customers WHERE email=%s'
    self.db_connection.cursor.execute(query, (self.email,))
    return self.db_connection.cursor.fetchone()[0]
  

# Category Class 
class Category:
  def __init__(self, db, category_name):
    self.db_connection = db
    self.category_name = category_name

  def add_to_db(self):
    query='INSERT INTO categories (category_name) VALUES (%s)'
    self.db_connection.cursor.execute(query, (self.category_name,))
    self.db_connection.db.commit()

  def get_category_id(self):
    query='SELECT category_id FROM categories WHERE category_name=%s'
    self.db_connection.cursor.execute(query, (self.category_name,))
    return self.db_connection.cursor.fetchone()[0]
  
