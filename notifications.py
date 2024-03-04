from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.system.createBot import bot, conn, cursor
from handlers.clients.states import menuStates
from keyboards import disabledNotificationKB, enableNotificationKB, settingsMenuKB

# Уведомления об истории
async def notifications(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
        photo = open('resources/images/settingsMenu.png', 'rb')
        await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption="Настройки"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=settingsMenuKB)
        await menuStates.settingsMenu.set()
    elif callback_query.data in ['on', 'off']:
        user_id = callback_query.from_user.id
        action = 'включены' if callback_query.data == 'on' else 'отключены'
        cursor.execute('INSERT INTO notifications (user_id) VALUES (?)', (user_id,)) if callback_query.data == 'on' else cursor.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
        conn.commit()
        await callback_query.answer(f'🔔 Уведомления {action}')
        photo = open('resources/images/notifications.png', 'rb')
        await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption=f"<b>Статус уведомлений:</b> {action}\n<i>Уведомления о новых историях в боте</i>", parse_mode='HTML'), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=disabledNotificationKB if callback_query.data == 'on' else enableNotificationKB)
        await menuStates.notifications.set()