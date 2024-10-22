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
  

# Product Class 
class Product:
  def __init__(self, db, product_name, price, quantity, description):
    self.db_connection = db
    self.product_name = product_name
    self.price = price
    self.quantity = quantity 
    self.description = description

  def add_to_db(self):
    query='INSERT INTO products (product_name, price, quantity, description) VALUE (%s, %s, %s, %s)'
    self.db_connection.cursor.execute(query, (self.product_name, self.price, self.quantity, self.description))
    self.db_connection.db.commit()
    print(f'Added Product: {self.product_name}, Price: {self.price}, Quantity: {self.quantity}, Description: {self.description}')

  def get_product_id(self):
    query='SELECT product_id FROM products WHERE product_name=%s'
    self.db_connection.cursor(query, (self.product_name,))
    return self.db_connection.cursor.fetchone()[0]
  
  def assign_to_category(self, category_id):
    query='INSERT INTO products_categories (product_id, category_id) VALUES (%s, %s)'
    self.db_connection.cursor.execute(query, self.get_product_id(), category_id)
    self.db_connection.db.commit()

  
# Cart class 
class Cart:
  def __init__(self, db, customer_id):
    self.db_connection = db
    self.customer_id = customer_id
    self.total_price = 0 

  def add_to_db(self):
    query='INSERT INTO carts (customer_id) VALUES (%s)'
    self.db_connection.cursor.execute(query, (self.customer_id,))
    self.db_connection.commit()
    print(f'Customer id {self.customer_id} created cart')

  def get_cart_id(self):
    query='SELECT cart_id FROM carts WHERE customer_id = %s'
    self.db_connection.cusor.execute(query, (self.customer_id,))
    return self.db_connection.cursor.fetchone()[0]
  
  def add_item(self, product_id, quantity):
    product_query = 'SELECT price, quantity FROM products WHERE product_id = %s'
    self.db_connection.cursor.exectue(product_query, (product_id,))
    product = self.db_connection.cursor.fetchone()
    if product and product[1] >= quantity:
      price = product[0] * quantity
      self.total_price += price 
      # Insert to cart_items 
      query='INSERT INTO cart_items (cart_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)'
      self.db_connection.cursor.execute(query, (self.get_cart_id(), product_id, quantity, price))
      # Update product stock 
      update_quantity_query = 'UPDATE products SET quantity = quantity - %s WHERE product_id = %s'
      self.db_connection.cursor.execute(update_quantity_query, (quantity, product_id))
    else: 
      print('Product out of stock or Invalid')

    self.db_connection.db.commit()

  def check_out(self):
    query='UPDATE carts SET total_price=%s WHERE cart_id=%s'
    self.db_connection.cursor.execute(query, (self.total_price, self.get_cart_id()))
    self.db_connection.db.commit()

# Order Class 
class Order:
  def __init__(self, db, customer_id, total_price):
    self.db_connection = db
    self.customer_id = customer_id
    self.total_price = total_price
    self.order_date = date.today()
    self.status = 'Pending'

  def place_order(self):
    query='INSERT INTO orders (customer_id, total_price, order_date, status) VALUES (%s, %s, %s, %s)'
    self.db_connection.cursor.execute(query, (self.customer_id, self.total_price, self.order_date, self.status))
    self.db_connection.db.commit()

  def update_status(self, new_status):
    query='UPDATE orders SET status = %s WHERE customer_id = %s'
    self.db_connection.cursor.execute(query, (new_status, self.customer_id))
    self.db_connection.db.commit()

# Review Class 



