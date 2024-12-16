
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
# uri = "mongodb+srv://princeanaba44:jQSYxgaLCO5G0Ql9@cluster0.gxtj7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
load_dotenv()

url = os.getenv("MONGODB_URL")

# Create a new client and connect to the server
client = MongoClient(url, server_api=ServerApi('1'))
db = client["sample_mflix"]

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)