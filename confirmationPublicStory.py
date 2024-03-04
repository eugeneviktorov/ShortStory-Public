from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.system.createBot import bot, conn, cursor
from handlers.clients.states import menuStates
from .storyNotificationHandler import storyNotificationHandler
from keyboards import choosingStoryActionKB, choosingStoryActionAdminKB, backKB

# Подтверждение публикации истории
async def confirmationPublicStory(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirmation':
        async with state.proxy() as data:
            category = data['category']
            theme = data['theme']
            text = data['text']
        # Передача данных в функцию записи данных базы данных
        await storyDB(category=category, theme=theme, text=text, complain='notVerified')
        # Уведомление о новой истории
        await storyNotificationHandler(callback_query)
        await callback_query.answer('✅ Ваша история опубликована!\n\nВы можете посмотреть её в меню "Прочитать историю" по выбранной вами категории истории.', show_alert=True)
        await mainMenuNavigation(callback_query, state)
    # Возращение к главному меню
    elif callback_query.data == 'mainMenu':
        await callback_query.answer('❌ Действие отменено!\n\nВаша история не опубликована. Ждем с нетерпением вашего творческого вклада!', show_alert=True)
        await mainMenuNavigation(callback_query, state)
    # Возвращение к написании истории
    elif callback_query.data == 'back':
        photo = open('resources/images/textStoryWrite.png', 'rb')
        await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "<b>Напишите вашу историю</b>\nИстория должна вмещаться в одно сообщение Telegram. Используемый формат до <b>4000</b> символов", parse_mode='HTML'), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=backKB)
        await menuStates.textStory.set()

# Навигация в главное меню:
async def mainMenuNavigation(callback_query: types.CallbackQuery, state: FSMContext):
    # Проверка, является ли пользователь администратором
    user_id = callback_query.from_user.id
    cursor.execute('SELECT * FROM administration WHERE user_id = ?', (user_id,))
    adminData = cursor.fetchone()
    # Пользователь является администратором
    if adminData is not None:
        keyboard = choosingStoryActionAdminKB
    # Пользователь не является администратором
    else:
        keyboard = choosingStoryActionKB
    photo = open('resources/images/mainMenu.png', 'rb')
    await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "Главное меню"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=keyboard)
    await state.finish()

# Запись истории в базу данных
async def storyDB(category: str, theme: str, text: str, complain: str):
    cursor.execute('INSERT INTO story (category, theme, text, complain) VALUES (?, ?, ?, ?)', (category, theme, text, complain))
    conn.commit()