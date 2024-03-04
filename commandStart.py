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
        # Проверка, является ли администратор пользователем
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        # Пользователь присутвует в базе данных, выдача клавиатуры для администратора
        if user_data is not None:
            photo = open('resources/images/mainMenu.png', 'rb')
            await message.answer_photo(photo=photo, caption="Главное меню", reply_markup=choosingStoryActionAdminKB)
        # Пользователь отсутсвует в базе данных, добавление и приветствие
        else:
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            photo = open('resources/images/newUser.png', 'rb')
            await message.answer_photo(photo=photo, caption="Бот ShortStory приветствует вас!\nВы в главном меню", reply_markup=choosingStoryActionAdminKB)
    # Пользователь не является администратором
    else:
        # Проверка, является ли пользователь пользователем
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        # Пользователь присутвует в базе данных, выдача клавиатуры для пользователя
        if user_data is not None:
            photo = open('resources/images/mainMenu.png', 'rb')
            await message.answer_photo(photo=photo, caption="Главное меню", reply_markup=choosingStoryActionKB)
        # Пользователя отсутсвует в базе данных, добавление и приветствие
        else:
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            photo = open('resources/images/newUser.png', 'rb')
            await message.answer_photo(photo=photo, caption="Бот ShortStory приветствует вас!\nВы в главном меню", reply_markup=choosingStoryActionKB)