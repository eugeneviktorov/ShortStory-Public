from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.system.createBot import conn, cursor
from keyboards import choosingStoryActionKB, choosingStoryActionAdminKB

# Начальная команда
async def commandStart(message: types.Message, state: FSMContext):
    if message.text or message.audio or message.document or message.animation or message.game or message.photo or message.sticker or message.video or message.voice or message.video_note or message.voice or message.location or message.venue or message.poll or message.dice or message.invoice or message.successful_payment:
        await startCommandHandler(message, state)

# Обработка команды старта и неизвестных команд
async def startCommandHandler(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    # Проверка, является ли пользователь администратором
    cursor.execute('SELECT * FROM administration WHERE user_id = ?', (user_id,))
    adminData = cursor.fetchone()
    # Пользователь является администратором
    if adminData is not None:
        keyboard = choosingStoryActionAdminKB
        await userDataStarting(message, state, user_id, keyboard)
    # Пользователь не является администратором
    else:
        keyboard = choosingStoryActionKB
        await userDataStarting(message, state, user_id, keyboard)

# Выдача сообщения пользователю на основе его статуса
async def userDataStarting(message: types.Message, state: FSMContext, user_id, keyboard):
    # Проверка, является ли пользователь пользователем
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    userData = cursor.fetchone()
    # Пользователь присутвует в базе данных, выдача клавиатуры для пользователя
    if userData is not None:
        photo = open('resources/images/mainMenu.png', 'rb')
        await message.answer_photo(photo=photo, caption="Главное меню", reply_markup=keyboard)
    # Пользователя отсутсвует в базе данных, добавление и приветствие
    else:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        photo = open('resources/images/newUser.png', 'rb')
        await message.answer_photo(photo=photo, caption="Бот ShortStory приветствует вас!\nВы в главном меню", reply_markup=keyboard)