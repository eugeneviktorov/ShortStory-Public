# Обработка неизвестной команды
async def startCommandHandler(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    # Проверка, является ли пользователь администратором
    cursor.execute('SELECT * FROM administration WHERE user_id = ?', (user_id,))
    admin_data = cursor.fetchone()
    # Пользователь является администратором
    if admin_data is not None:
        # Проверка, является ли администратор пользователем
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        # Пользователь уже есть в базе данных, выдача клавиатуры для администратора
        if user_data is not None:
            photo = open('resources/images/mainMenu.png', 'rb')
            await message.answer_photo(photo=photo, caption="Главное меню", reply_markup=choosingStoryActionAdminKB)
        # Пользователя нет в базе данных, добавление и приветствие
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
        # Пользователь уже есть в базе данных, выдача клавиатуры для пользователя
        if user_data is not None:
            photo = open('resources/images/mainMenu.png', 'rb')
            await message.answer_photo(photo=photo, caption="Главное меню", reply_markup=choosingStoryActionKB)
        # Пользователя нет в базе данных, добавление и приветствие
        else:
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            photo = open('resources/images/newUser.png', 'rb')
            await message.answer_photo(photo=photo, caption="Бот ShortStory приветствует вас!\nВы в главном меню", reply_markup=choosingStoryActionKB)