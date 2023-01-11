from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import math
import sqlite3
from pyqiwip2p import QiwiP2P
import random
import time

bot = Bot(token = "5649227479:AAE7pVofGnQ1z4oQunuSNLBV1ZtvRpvHYF8")
dp = Dispatcher(bot)
qiwip2p = QiwiP2P(auth_key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImwzNTl3MC0wMCIsInVzZXJfaWQiOiI3OTIxMjUyNzM1NSIsInNlY3JldCI6IjY3NDVlYTcyZTY4YmMyMTU1OThmMjlhM2RiNTY0NTY2ZTk3ZDhmYjFmZTYxNDM5M2RiMGU3NWFhOGYwZjllNmYifX0=")





@dp.message_handler(commands=['start'])
async def start(message : types.Message):
    try:
        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        if cursor.execute("SELECT user_id FROM user_data WHERE user_id = " + str(message.from_user.id)).fetchone() == None:
            cursor.execute("INSERT INTO user_data (user_id) VALUES (" + str(message.from_user.id) + ")")
            conn.commit()
    except sqlite3.Error as error:
        print("Error")
    markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    balance = KeyboardButton("💲 Пополнить баланс")
    buy = KeyboardButton("🍯 Купить голду")
    support = KeyboardButton("🧑‍💻 Поддержка")
    profile = KeyboardButton("👤 Профиль")
    exchange_rate = KeyboardButton("📉 Курс")
    reviews = KeyboardButton("😄 Отзывы")
    markup.add(balance, buy, support, profile, exchange_rate, reviews)
    msg = "▶️ Для продолжения выбери нужную команду на клавиатуре\n👇\n🙋‍♂️ Если есть дополнительные вопросы по поводу бота, обратитесь в Тех.Поддержку\n📊 Курс: 55₽ за 100 голды"
    await message.answer(msg, reply_markup = markup)


@dp.message_handler()
async def getTextInfo(message : types.Message):
    stage = "menu"
    try:
        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        stage = cursor.execute("SELECT status FROM user_data WHERE user_id = " + str(message.from_user.id)).fetchone()[0]
    except sqlite3.Error as error:
        print("Error")
    if message.text == "Главное меню":
        try:
            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE user_data SET status = 'menu' WHERE user_id = " + str(message.from_user.id))
            conn.commit()
        except sqlite3.Error as error:
            print("Error")
        await start(message)
    if stage == "menu":
        if message.text == "📉 Курс":
            await message.answer("📉 Курс: 55 рублей за 100 голды")
        elif message.text == "🧑‍💻 Поддержка":
            msg = "1. Почему я пополняю в гривнах, а мне пришло меньше рублей, чем пишет в интернете?\n2. Сколько по времени выводят золото?\n3. Почему так долго выводят золото?\n4. Почему мне не пришли деньги?\n5. Безопасно ли у вас покупать?"
            markup = InlineKeyboardMarkup(row_width = 3)
            first = InlineKeyboardButton("1", callback_data = "one_q")
            second = InlineKeyboardButton("2", callback_data = "two_q")
            third = InlineKeyboardButton("3", callback_data = "three_q")
            fourth = InlineKeyboardButton("4", callback_data = "four_q")
            fifth = InlineKeyboardButton("5", callback_data = "five_q")
            contact = InlineKeyboardButton("Связаться", callback_data = "contact_q")
            markup.add(first, second, third, fourth, fifth, contact)
            await message.answer(msg, reply_markup = markup)
        elif message.text == "😄 Отзывы":
            await message.answer("😄 Наши отзывы: t.me/Standsseller")
        elif message.text == "💲 Пополнить баланс":
            try:
                conn = sqlite3.connect("accounts.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE user_data SET status = 'add balance' WHERE user_id = " + str(message.from_user.id))
                conn.commit()
            except sqlite3.Error as error:
                print("Error")
            msg = "Введите сумму, которую вы хотите пополнить на баланс.\nНапример: 55\n\n❗️Минимальная сумма пополнения 55₽\n❗ Обязательно введите целое число"
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
            menu = types.KeyboardButton("Главное меню")
            markup.add(menu)
            await message.answer(msg, reply_markup = markup)
        elif message.text == "👤 Профиль":
            try:
                conn = sqlite3.connect("accounts.db")
                cursor = conn.cursor()
                data = cursor.execute("SELECT * FROM user_data WHERE user_id = " + str(message.from_user.id)).fetchone()
                msg = "Информация о " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "\nUID: " + str(data[1]) + "\nID: " + str(data[0]) + "\n\n🏦 Баланс:\n💵 Рублей: " + str(data[2]) + " руб\n\n💵 Всего пополнено: на " + str(data[3]) + "₽\n🍯 Всего куплено: " + str(data[4]) + "G"
                await message.answer(msg)
            except sqlite3.Error as error:
                print("Error")
        elif message.text == "🍯 Купить голду":
            try:
                conn = sqlite3.connect("accounts.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE user_data SET status = 'buy gold' WHERE user_id = " + str(message.from_user.id))
                data = cursor.execute("SELECT rub_balance FROM user_data WHERE user_id = " + str(message.from_user.id)).fetchone()
                conn.commit()
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
                markup.add(types.KeyboardButton("Главное меню"))
                balance = data[0]
                max_gold = math.floor(int(balance) / 55 * 100)
                msg = "💸 Выберите количество голды, которое вы хотите купить\n🏦 Ваш баланс: " + str(balance) + " \n🍯 Количество голды, которое вы можете купить: " + str(max_gold)
                await message.answer(msg, reply_markup = markup)
            except sqlite3.Error as error:
                print("Error")
    elif stage == "add balance":
        if message.text.isdigit() and int(message.text) >= 55 and int(message.text) < 100000:
            try:
                conn = sqlite3.connect("accounts.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE user_data SET status = 'payment' WHERE user_id = " + str(message.from_user.id))
                conn.commit()
            except sqlite3.Error as error:
                print("Error")
            payment_count = message.text
            msg = "⭐️ За " + payment_count + " рублей вы сможете купить " + str(math.floor(int(payment_count) * 100 / 55)) + " золота\n🖋 Выберите наиболее удобный для вас способ оплаты"
            markup = types.InlineKeyboardMarkup(row_width = 1) #🥝
            comment = str(message.from_user.id) + "_" + str(random.randint(10000, 99999))
            bill = qiwip2p.bill(amount = int(payment_count), lifetime = 5, comment = comment)
            payment = types.InlineKeyboardButton("Оплатить " + payment_count + " рублей", bill.pay_url)
            check_btn_data = "c_" + str(bill.bill_id) + " " + payment_count + " " + str(message.from_user.id)
            check_pay = types.InlineKeyboardButton("Проверить оплату", callback_data = check_btn_data)
            markup.add(payment, check_pay)
            await message.answer(msg, reply_markup = markup)
        else:
            if message.text != "Главное меню":
                await message.answer("Ошибка ❗\nВведите сумму от 55 до 100.000 рублей 💸")
    elif stage == "buy gold":
        try:
            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            data = cursor.execute("SELECT rub_balance, all_gold FROM user_data WHERE user_id = " + str(message.from_user.id)).fetchone()
            balance = int(data[0])
            all_gold = int(data[1])
            max_gold = math.floor(int(balance) / 55 * 100)
            if message.text.isdigit():
                if int(message.text) >= 100:
                    if int(message.text) <= max_gold:
                        try:
                            cost = math.floor(int(message.text) / 100 * 55)
                            balance = balance - cost
                            all_gold = all_gold + int(message.text)
                            msg = "Покупка прошла успешно✅\n\nКуплено голды: " + message.text + "\n\nПерешлите данное сообщение администратору - @Standssellerr для получения голды."
                            conn = sqlite3.connect("accounts.db")
                            cursor = conn.cursor()
                            cursor.execute("UPDATE user_data SET rub_balance = " + str(balance) + " WHERE user_id = " + str(message.from_user.id))
                            cursor.execute("UPDATE user_data SET all_gold = " + str(all_gold) + " WHERE user_id = " + str(message.from_user.id))
                            conn.commit()
                            await message.answer(msg)
                        except sqlite3.Error as error:
                            print("Error")
                    else:
                        if message.text != "Главное меню":
                            await message.answer("Недостаточно средств на Вашем балансе❌")
                else:
                    if message.text != "Главное меню":
                        await message.answer("Ошибка❗\nМинимальное количество голды для покупки - 100🍯")
            else:
                if message.text != "Главное меню":
                    await message.answer("Ошибка❗\nВведите количество голды, которое вы хотите купить🍯")
        except sqlite3.Error as error:
            print("Error")



@dp.callback_query_handler()
async def callback(call_data: types.CallbackQuery):
    if "c_" in call_data.data:
        data = call_data.data[2:].split(" ")
        bill_id = data[0]
        payment_count = int(data[1])
        user_id = data[2]
        if str(qiwip2p.check(bill_id=bill_id).status) == "PAID":
            try:
                conn = sqlite3.connect("accounts.db")
                cursor = conn.cursor()
                old_data = cursor.execute("SELECT rub_balance, all_rub FROM user_data WHERE user_id = " + str(user_id)).fetchone()
                rub = int(old_data[0]) + payment_count
                all_rub = int(old_data[1]) + payment_count
                cursor.execute("UPDATE user_data SET rub_balance = " + str(rub) + " WHERE user_id = " + user_id)
                cursor.execute("UPDATE user_data SET all_rub = " + str(all_rub) + " WHERE user_id = " + user_id)
                conn.commit()
                await call_data.message.answer("Вы успешно пополнили свой баланс на " + str(payment_count) + " рублей 💸")
            except sqlite3.Error as error:
                print("Error")
        else:
            await call_data.message.answer("Ошибка ❗\nВы не оплатили счет 💸")
    if call_data.data == 'one_q':
        markup = types.InlineKeyboardMarkup(row_width = 2)
        contact = types.InlineKeyboardButton("Связаться", callback_data = "contact_q")
        back = types.InlineKeyboardButton("Назад", callback_data = "back_q")
        markup.add(contact, back)
        await call_data.message.edit_text('Мы не являемся биржей валют, вы у нас покупаете золото, а не рубли. То есть, мы переводим ваши гривны в золото. После, золото в рубли.', reply_markup = markup)
    elif call_data.data == "two_q":
        markup = types.InlineKeyboardMarkup(row_width=2)
        contact = types.InlineKeyboardButton("Связаться", callback_data="contact_q")
        back = types.InlineKeyboardButton("Назад", callback_data="back_q")
        markup.add(contact, back)
        await call_data.message.edit_text("Вывод золота происходит до 24 часов от запроса на вывод. Но в большинстве вывод происходит от нескольких секунд до часа.", reply_markup = markup)
    elif call_data.data == "three_q":
        markup = types.InlineKeyboardMarkup(row_width=2)
        contact = types.InlineKeyboardButton("Связаться", callback_data="contact_q")
        back = types.InlineKeyboardButton("Назад", callback_data="back_q")
        markup.add(contact, back)
        await call_data.message.edit_text("Вывод золота занимает до 24 часов. Но мы стараемся как можно быстрее вывести вам золото. В большинстве случаев, есть очередь, и пока она дойдёт до вас, может пройти немного времени. Но если вы уже пол часа как на 1 месте, это может быть из-за проблем с рынком ( сложно искать скин) или работник взял перерыв.", reply_markup = markup)
    elif call_data.data == "four_q":
        markup = types.InlineKeyboardMarkup(row_width=2)
        contact = types.InlineKeyboardButton("Связаться", callback_data="contact_q")
        back = types.InlineKeyboardButton("Назад", callback_data="back_q")
        markup.add(contact, back)
        await call_data.message.edit_text("Если вы пополняли через QIWI, то найдите сообщение где вам выдали ссылку на оплату, и под этим сообщением будет кнопка «Проверить оплату» нажмите её. Но если вы пополняли другим способом, то вы, возможно, скинули боту чек файлом. В подобном случае, нажмите: ' Пополнить баланс '; укажите сумму; ' Другим способом '; ' Отправить чек '. После, отправьте скриншот чека.", reply_markup = markup)
    elif call_data.data == "five_q":
        markup = types.InlineKeyboardMarkup(row_width=2)
        contact = types.InlineKeyboardButton("Связаться", callback_data="contact_q")
        back = types.InlineKeyboardButton("Назад", callback_data="back_q")
        markup.add(contact, back)
        await call_data.message.edit_text("Весь товар, который продаётся в боте, получен честным путём. Если вы сомневаетесь в безопасности, то лучше покупать в игре.", reply_markup = markup)
    elif call_data.data == "contact_q":
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton("Назад", callback_data = "back_q")
        markup.add(back)
        await call_data.message.edit_text("Остались вопросы ❓ - обращайтесь к @Standssellerr", reply_markup = markup)
    elif call_data.data == "back_q":
        msg = "1. Почему я пополняю в гривнах, а мне пришло меньше рублей, чем пишет в интернете?\n2. Сколько по времени выводят золото?\n3. Почему так долго выводят золото?\n4. Почему мне не пришли деньги?\n5. Безопасно ли у вас покупать?"
        markup = types.InlineKeyboardMarkup(row_width=3)
        first = types.InlineKeyboardButton("1", callback_data="one_q")
        second = types.InlineKeyboardButton("2", callback_data="two_q")
        third = types.InlineKeyboardButton("3", callback_data="three_q")
        fourth = types.InlineKeyboardButton("4", callback_data="four_q")
        fifth = types.InlineKeyboardButton("5", callback_data="five_q")
        contact = types.InlineKeyboardButton("Связаться", callback_data="contact_q")
        markup.add(first, second, third, fourth, fifth, contact)
        await call_data.message.edit_text(msg, reply_markup = markup)


executor.start_polling(dp, skip_updates = True)