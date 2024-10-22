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
    self.db_connection.cursor.execute(query, (self.product_name,))
    return self.db_connection.cursor.fetchone()[0]
  
  def assign_to_category(self, category_id):
    query='INSERT INTO products_categories (product_id, category_id) VALUES (%s, %s)'
    self.db_connection.cursor.execute(query, (self.get_product_id(), category_id))
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
    self.db_connection.db.commit()
    print(f'Customer id {self.customer_id} created cart')

  def get_cart_id(self):
    query='SELECT cart_id FROM carts WHERE customer_id = %s'
    self.db_connection.cursor.execute(query, (self.customer_id,))
    return self.db_connection.cursor.fetchone()[0]
  
  def add_item(self, product_id, quantity):
    product_query = 'SELECT price, quantity FROM products WHERE product_id = %s'
    self.db_connection.cursor.execute(product_query, (product_id,))
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

  def remove_item(self, product_id):
    # Create var for total Quantity 
    total_quantity = 0

    # GET cart_item_id 
    get_cart_item_id_query = 'SELECT quantity FROM cart_items WHERE product_id=%s and cart_id=%s'
    self.db_connection.cursor.execute(get_cart_item_id_query, (product_id, self.get_cart_id()))
    quantities = self.db_connection.cursor.fetchall()

    # Check if customer add 2 or more the same item
    if len(quantities) > 1 :
      for quanity in quantities:
        total_quantity += quanity[0]
    else : 
      total_quantity = quantities[0][0]

    # Update quantiy in Product 
    update_quantity_query = 'UPDATE products SET quantity = %s WHERE product_id = %s'
    self.db_connection.cursor.execute(update_quantity_query, (total_quantity, product_id))
    
    # Remove item from cart 
    query = 'DELETE FROM cart_items WHERE product_id=%s and cart_id=%s'
    self.db_connection.cursor.execute(query, (product_id, self.get_cart_id()))

    # commit 
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
class Review:
  def __init__(self, db, product_id, customer_id, rating, comment):
    self.db_connection = db
    self. product_id = product_id
    self.customer_id = customer_id 
    self.rating = rating
    self.comment = comment
    self.review_date = date.today()

  def add_review(self):
    query = 'INSERT INTO reviews (product_id, customer_id, rating, comment, review_date) VALUES (%s, %s, %s, %s, %s)'
    self.db_connection.cursor.execute(query, (self.product_id, self.customer_id, self.rating, self.comment, self.review_date))
    self.db_connection.db.commit()


database = Database()
# Create Customer 
tim = Customer(database, 'Tim', 'tim@gmail.com', '1234567')
tim_id = tim.get_customer_id()

# Create new Category 
electricity = Category(database, 'Electric')
electricity_id = (electricity.get_category_id())

# Create a new product and assign it to the electronics category
iphone = Product(database, 'Iphone', 2000, 20, 'Highest Quality Phone')
iphone_id = iphone.get_product_id()

# Create cart for Tim 
tim_cart = Cart(database, tim_id)
tim_cart_id = (tim_cart.get_cart_id())

# Add Item to tim cart
# tim_cart.add_item(iphone_id, 10)

# Check out 
tim_cart.remove_item(iphone_id)