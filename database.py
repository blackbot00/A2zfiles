import motor.motor_asyncio
from datetime import datetime, timedelta
from config import Config

client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
db = client.filter_bot

users = db.users
missing_files = db.missing_files

async def get_user(user_id):
    user = await users.find_one({"_id": user_id})
    if not user:
        return {"_id": user_id, "total_count": 0, "daily_count": 0, "last_reset": datetime.now(), "is_premium": False}
    return user

async def update_user_limit(user_id, count):
    await users.update_one({"_id": user_id}, {"$inc": {"total_count": count, "daily_count": count}}, upsert=True)

async def log_missing_file(query):
    await missing_files.update_one(
        {"query": query.lower()}, 
        {"$set": {"time": datetime.now()}, "$inc": {"count": 1}}, 
        upsert=True
         )
      
