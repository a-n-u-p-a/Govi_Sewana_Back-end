from django.db import models
from db_connection import db

# Create your models here.
user_collection = db['User']
yield_collection = db['Crop_Yield']
excess_collection = db['Crop_Excess']
