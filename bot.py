from pyrogram import Client, filters, types
from config import Config
from database import get_user, update_user_limit, log_missing_file, missing_files
from datetime import datetime, timedelta

app = Client("FilterBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

@app.on_message(filters.text & filters.group)
async def filter_logic(client, message):
    user_id = message.from_user.id
    query = message.text
    
    user_data = await get_user(user_id)
    
    # Limit Check
    if not user_data['is_premium']:
        if user_data['total_count'] >= 100 and user_data['daily_count'] >= 10:
            return await message.reply("Daily limit over! Buy Premium using Stars.")

    # Search Logic (Simplified)
    files = [] # Inga unga indexing logic-ah connect pannanum
    
    if not files:
        await log_missing_file(query)
        return await message.reply("File Not Found. Added to request list.")

    # File send panna apram count update
    await update_user_limit(user_id, 1)

@app.on_message(filters.command("missing") & filters.user("admin_id"))
async def show_missing(client, message):
    last_7_days = datetime.now() - timedelta(days=7)
    cursor = missing_files.find({"time": {"$gte": last_7_days}}).sort("count", -1)
    
    text = "**Last 7 Days Requested Files:**\n\n"
    async for doc in cursor:
        text += f"• {doc['query']} (Requested {doc['count']} times)\n"
    
    await message.reply(text)

app.run()

