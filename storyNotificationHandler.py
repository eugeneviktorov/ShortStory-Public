from aiogram import types
from handlers.system.createBot import cursor, dp
from handlers.system.navigationStoryHandler import unpinMessageHandler
from keyboards import navigationNotificationKB

# Уведомление о новой истории
async def storyNotificationHandler(callback_query: types.CallbackQuery):
    await unpinMessageHandler(dp, callback_query.message.chat.id)
    cursor.execute('SELECT user_id FROM notifications')
    users = cursor.fetchall()
    for user in users:
        user_id = user[0]
        try:
            message = await dp.bot.send_message(user_id, text="<b><i>🔔 Опубликована новая история</i></b>", parse_mode='HTML', reply_markup=navigationNotificationKB)
            await dp.bot.pin_chat_message(user_id, message.message_id)
            await dp.bot.delete_message(user_id, message_id=message.message_id+1)
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")