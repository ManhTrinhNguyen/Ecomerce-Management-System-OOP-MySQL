import mysql.connector 
import os 
from dotenv import load_dotenv

load_dotenv()

class Database:
  def __init__(self):
    self.db = mysql.connector.connect(
      host='localhost',
      user=os.getenv('DB_USER'),
      password=os.getenv('DB_PASSWORD'),
      database='Ecomerce_System'
    )
    self.cursor = self.db.cursor()
