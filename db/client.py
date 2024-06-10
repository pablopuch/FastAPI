from pymongo import MongoClient

# db_client = MongoClient().local


db_client = MongoClient("mongodb+srv://root:Pgl82kuT46aLsJni@cluster0.wzehgjm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test
