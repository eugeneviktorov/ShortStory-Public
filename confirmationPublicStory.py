# Подтверждение публикации истории
async def confirmationPublicStory(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirmation':
        async with state.proxy() as data:
            category = data['category']
            theme = data['theme']
            text = data['text']
        # Передача данных в функцию записи данных базы данных
        await storyDB(category=category, theme=theme, text=text, complain='notVerified')
        await callback_query.answer('✅ Ваша история опубликована!\n\nВы можете посмотреть её в меню "Прочитать историю" по выбранной вами категории истории.', show_alert=True)
        # Проверка, является ли пользователь администратором
        cursor.execute('SELECT user_id FROM administration')
        admin_data = cursor.fetchone()
        # Пользователь является администратором
        if admin_data is not None:
            photo = open('resources/images/mainMenu.png', 'rb')
            await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "Главное меню"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=choosingStoryActionAdminKB)
            await state.finish()
        # Пользователь не является администратором
        else:
            photo = open('resources/images/mainMenu.png', 'rb')
            await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "Главное меню"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=choosingStoryActionKB)
            await state.finish()
    # Возвращение к написании истории
    elif callback_query.data == 'back':
        photo = open('resources/images/textStoryWrite.png', 'rb')
        await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "*Напишите вашу историю*\nИстория должна вмещаться в одно сообщение Telegram. Используемый формат до *4000* символов", parse_mode='Markdown'), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=backKB)
        await menuStates.textStory.set()
    # Возращение к главному меню
    elif callback_query.data == 'mainMenu':
        await callback_query.answer('❌ Действие отменено!\n\nВаша история не опубликована. Ждем с нетерпением вашего творческого вклада!', show_alert=True)
        # Проверка, является ли пользователь администратором
        cursor.execute('SELECT user_id FROM administration')
        admin_data = cursor.fetchone()
        # Пользователь является администратором
        if admin_data is not None:
            photo = open('resources/images/mainMenu.png', 'rb')
            await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "Главное меню"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=choosingStoryActionAdminKB)
            await state.finish()
        # Пользователь не является администратором
        else:
            photo = open('resources/images/mainMenu.png', 'rb')
            await bot.edit_message_media(media=types.InputMediaPhoto(type='photo', media=photo, caption = "Главное меню"), chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=choosingStoryActionKB)
            await state.finish()

# Запись истории в базу данных
async def storyDB(category: str, theme: str, text: str, complain: str):
    cursor.execute('INSERT INTO story (category, theme, text, complain) VALUES (?, ?, ?, ?)', (category, theme, text, complain))
    conn.commit()