from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.system.createBot import bot, conn, cursor
from handlers.clients.states import menuStates
from keyboards import settingsMenuKB

# Уведомления об истории
async def dataProfile(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if callback_query.data == 'back':
        try: 
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            await callback_query.answer(f'✅ Вы снова пользователь бота!')
        except:
            pass
        photo = open('resources/images/settingsMenu.png', 'rb')
        await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption="Настройки"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=settingsMenuKB)
        await menuStates.settingsMenu.set()
        # Удаление персональных данных из базы данных
    elif callback_query.data == 'deleteDataProfile':
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        userData = cursor.fetchone()
        # Пользователь присутствует в базе данных
        if userData is not None:
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
            conn.commit()
            await callback_query.answer(f'✅ Данные успешно удалены!\n\nЕсли вы больше не хотите пользоваться ботом, не забудьте остановить его и заблокировать. Надеемся, что вы вернётесь к историям!\n\nС уважением,\nКоманда ShortStory', show_alert=True)
        # Пользователь отсутсвует в базе данных
        else:
            await callback_query.answer(f'❌ Ваши данные отсутсвуют!\n\nНажмите на кнопку "Назад" или используйте команду "/start" чтобы стать пользователем.', show_alert=True)