
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Объект бота
APTOKEN = ""
ADMIN = 
#admin panel
kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.InlineKeyboardButton(text = "Рассылка"))
kb.add(types.InlineKeyboardButton(text = "Добавить в ЧС"))
kb.add(types.InlineKeyboardButton(text = "Убрать из ЧС"))
kb.add(types.InlineKeyboardButton(text = "Статистика"))
kb.add(types.InlineKeyboardButton(text = "Список участников"))
kb.add(types.InlineKeyboardButton(text = "Выдать роль"))
kb.add(types.InlineKeyboardButton(text = "Test"))
#user panel
mainkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttonss = ["Расписание", "Настройка новостей"]
buttonss1 = ["Инициативы","FAQ"]
mainkeyboard.add(*buttonss)
mainkeyboard.add(*buttonss1)
storage = MemoryStorage()
bot = Bot(token=APTOKEN)
# Диспетчер для бота
dp = Dispatcher(bot,storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER,name_user TEXT,Role TEXT , block INTEGER,NewsGroup TEXT, NewsAll TEXT);""")
conn.commit()

class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()
    RoleList = State()
    Test = State()
#@dp.message_handler(commands = "Student")
#async def hanadler(message: types.Message, state: FSMContext):
#  if message.chat.id == ADMIN:
#    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#    keyboard.add(types.InlineKeyboardButton(text="Назад"))
#    await message.answer('Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
#    await dialog.LeaderList()

#Вход в личный кабинет админа
@dp.message_handler(commands=['admin'])
async def start(message: types.Message):
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if message.from_user.id == ADMIN:
    await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=kb)
  else:
      if result is None:
        await message.answer('Это функциия недоступна')
      else:
        await message.answer('Это функциия недоступна')
@dp.message_handler(content_types=['text'], text='Назад')
async def start(message: types.Message):
    await message.reply (message.text,reply_markup = mainkeyboard)
@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: types.Message):
  await dialog.spam.set()
  await message.answer('Напиши текст рассылки')
@dp.message_handler(state=dialog.spam)
async def start_spam(message: types.Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer('Главное меню', reply_markup=kb)
    await state.finish()
  else:
    cur = conn.cursor()
    cur.execute(f'''SELECT user_id FROM users''')
    spam_base = cur.fetchall()
    for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], message.text)
            await message.answer('Рассылка завершена', reply_markup=kb)
            await state.finish()
@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
  if message.chat.id == ADMIN:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text="Отмена"))
    await message.answer('Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
    await dialog.blacklist.set()
@dp.message_handler(state=dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
  if message.text == 'Отмена':
    await message.answer('Отмена! Возвращаю назад.', reply_markup=kb)
    await state.finish()
  else:
    if message.text.isdigit():
      cur = conn.cursor()
      cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
      result = cur.fetchall()
      if len(result) == 0:
        await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb)
        await state.finish()
      else:
        a = result[0]
        id = a[0]
        if id == 0:
          cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
          conn.commit()
          await message.answer('Пользователь успешно добавлен в ЧС.', reply_markup=kb)
          await state.finish()
          await bot.send_message(message.text, 'Ты был забанен Администрацией')
        else:
          await message.answer('Данный пользователь уже получил бан', reply_markup=kb)
          await state.finish()
    else:
      await message.answer('Ты вводишь буквы...\n\nВведи ID')
@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if result is None:
    if message.chat.id == ADMIN:
      keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
      keyboard.add(types.InlineKeyboardButton(text="Отмена"))
  await message.answer('Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
  await dialog.whitelist.set()
@dp.message_handler(state=dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
  if message.text == 'Отмена':
    await message.answer('Отмена! Возвращаю назад.', reply_markup=kb)
    await state.finish()
  else:
    if message.text.isdigit():
      cur = conn.cursor()
      cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
      result = cur.fetchall()
      conn.commit()
      if len(result) == 0:
        await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb)
        await state.finish()
      else:
        a = result[0]
        id = a[0]
        if id == 1:
          cur = conn.cursor()
          cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
          conn.commit()
          await message.answer('Пользователь успешно разбанен.', reply_markup=kb)
          await state.finish()
          await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
        else:
          await message.answer('Данный пользователь не получал бан.', reply_markup=kb)
          await state.finish()
    else:
        await message.answer('Ты вводишь буквы...\n\nВведи ID')
@dp.message_handler(content_types=['text'], text='Статистика')
async def hfandler(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    cur.execute('''select * from users''')
    results = cur.fetchall()
    await message.answer(f'Людей которые когда либо заходили в бота: {len(results)}')
@dp.message_handler(content_types =['text'],text = 'Список участников')
async def SelectListId(message:types.Message,state:FSMContext):
    cur = conn.cursor()
    cur.execute(f'''SELECT user_id FROM users''')
    records = cur.fetchall()
    for z in range(len(records)):
        await message.answer(records[z][0], reply_markup=kb)
        await state.finish()
@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if result is None:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cur.fetchone()
        if entry is None:
          cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}','{message.from_user.first_name}','Student','0','ВКЛ','ВКЛ')''')
          conn.commit()
    await message.answer("Здравствуйте, " + message.from_user.first_name + " ,для авторизации в боте напишите команду /login")
@dp.message_handler(commands = "login")
async def cmd_login (message:types.Message):
    inline_btn_1 = InlineKeyboardButton('Регистрация', callback_data='button1')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    await message.answer("Нажмите на кнопку ниже для регистрации",reply_markup=inline_kb1)
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def registration (callback_query: types.CallbackQuery,state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы успешно зарегистрировались',reply_markup = mainkeyboard)
@dp.message_handler(content_types =['text'],text = 'Настройка новостей')
async def cmd_news (message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Статус", "Назад"]
    keyboard.add(*buttons)
    await message.answer(message.text,reply_markup = keyboard)
@dp.message_handler(content_types =['text'],text = 'Статус')
async def cmd_news (message:types.Message):
    cur = conn.cursor()
    cur.execute(f"SELECT NewsGroup,NewsAll FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchall()
    print(result)
    await message.answer ("Все новости: " + result[0][0] + "— нажми /switch1 для изменения\n" + "Новости для группы: " + result[0][1] + " — нажми /switch2 для изменения")
@dp.message_handler(commands = "switch1")
async def EditNewsAll (message:types.Message):
    cur = conn.cursor()
    cur.execute(f"SELECT NewsAll FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchall()
    print (result[0][0])
    if result[0][0] =='ВКЛ':
             cur.execute(f"UPDATE users SET NewsAll = 'ВЫКЛ' WHERE user_id = {message.chat.id}")
             conn.commit()
    elif result[0][0] == "ВЫКЛ":
             cur.execute(f"UPDATE users SET NewsAll = 'ВКЛ' WHERE user_id = {message.chat.id}")
             conn.commit()
    await message.reply("Статус успешно изменён")
@dp.message_handler(commands = "switch2")
async def EditNewsAll (message:types.Message):
    cur = conn.cursor()
    cur.execute(f"SELECT NewsGroup FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchall()
    if result[0][0] == "ВКЛ":
             cur.execute(f"UPDATE users SET NewsGroup = 'ВЫКЛ' WHERE user_id = {message.chat.id}")
             conn.commit()
    if result[0][0] == "ВЫКЛ":
             cur.execute(f"UPDATE users SET NewsGroup = 'ВКЛ' WHERE user_id = {message.chat.id}")
             conn.commit()
    await message.reply("Статус успешно изменён")
dp.register_message_handler(cmd_test2, commands="test2")
@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)
    await message.reply("Вы заблокированы")
from aiogram.utils.exceptions import BotBlocked
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
