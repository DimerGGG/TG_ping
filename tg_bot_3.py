import ctypes
import sys
import time
import threading
import ping3
import telebot
import win32gui
from configobj import ConfigObj
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Загрузка конфигурационного файла
config = ConfigObj('config.ini')

# Получение данных из конфигурации
BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
IP_ADDRESS = config['DEFAULT']['IP_ADRESS']
AWAIT = int(config['DEFAULT']['AWAIT'])
ID = int(config['DEFAULT']['ID'])

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Переменная для хранения предыдущего состояния сервера
prev_status = None

# Функция для минимизации окна консоли
def minimize_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 6)  # SW_MINIMIZE = 6

# Функция для проверки статуса сервера
def check_server_status(ip):
    return ping3.ping(ip, timeout=1) is not None

# Функция для отправки статуса сервера в личные сообщения
def send_server_status():
    global prev_status
    while True:
        current_status = "client is UP" if check_server_status(IP_ADDRESS) else "client is DOWN"
        if current_status != prev_status:
            bot.send_message(ID, current_status)
            print(current_status)
            prev_status = current_status
        time.sleep(AWAIT)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для мониторинга статуса сервера. Отправляю уведомления о смене статуса сервера.")

# Создание значка для трея
def create_image():
    width = 64
    height = 64
    color1 = "black"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

# Функция для выхода из программы
def on_quit(icon, item):
    icon.stop()
    sys.exit()

# Запуск функции отправки статуса сервера в отдельном потоке
def start_server_status():
    threading.Thread(target=send_server_status).start()

# Основная функция для запуска программы
def main():
    minimize_console()

    # Создание значка в трее
    icon = Icon("Server Monitor")
    icon.icon = create_image()
    icon.title = "Server Monitor"
    icon.menu = Menu(
        MenuItem("Exit", on_quit)
    )

    # Запуск мониторинга сервера
    start_server_status()

    # Запуск значка в трее
    icon.run()

if __name__ == "__main__":
    main()