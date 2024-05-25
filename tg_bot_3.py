import ctypes
import sys
import time
import threading
from pythonping import ping
import telebot
from configobj import ConfigObj
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import logging

# Загрузка конфигурационного файла
config = ConfigObj('config.ini')

# Получение данных из конфигурации
BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
IP_ADDRESS = config['DEFAULT']['IP_ADRESS']
AWAIT = int(config['DEFAULT']['AWAIT'])
ID = int(config['DEFAULT']['ID'])
DEBUG = int(config['DEFAULT'].get('DEBUG', 0))
CHECK_COUNT = int(config['DEFAULT'].get('CHECK_COUNT', 3))

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server_monitor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)
logger.debug("Бот инициализирован")

# Переменная для хранения предыдущего состояния сервера
prev_status = None
exit_event = threading.Event()

# Функция для минимизации окна консоли
def minimize_console():
    logger.debug("Минимизация окна консоли")
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 6)  # SW_MINIMIZE = 6

# Функция для проверки статуса сервера
def check_server_status(ip):
    logger.debug(f"Проверка статуса сервера: {ip}")
    response = ping(ip, count=1, timeout=1)
    result = response.success()
    logger.debug(f"Результат проверки: {'UP' if result else 'DOWN'}")
    return result

# Функция для отправки статуса сервера в личные сообщения
def send_server_status():
    global prev_status
    logger.debug("Запуск функции отправки статуса сервера")
    while not exit_event.is_set():
        statuses = [check_server_status(IP_ADDRESS) for _ in range(CHECK_COUNT)]
        current_status = "client is UP" if all(statuses) else "client is DOWN"
        logger.debug(f"Текущий статус: {current_status}")
        if current_status != prev_status:
            bot.send_message(ID, current_status)
            logger.info(f"Статус изменен: {current_status}")
            prev_status = current_status
        exit_event.wait(AWAIT)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.debug("Получена команда /start")
    bot.reply_to(message, "Привет! Я бот для мониторинга статуса сервера. Отправляю уведомления о смене статуса сервера.")
    logger.info("Команда /start обработана")

# Создание значка для трея
def create_image():
    logger.debug("Создание изображения для трея")
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
    logger.debug("Выход из программы")
    exit_event.set()
    bot.stop_polling()
    icon.stop()
    logger.info("Программа завершена")
    sys.exit(0)

# Запуск функции отправки статуса сервера в отдельном потоке
def start_server_status():
    logger.debug("Запуск мониторинга сервера в отдельном потоке")
    threading.Thread(target=send_server_status, daemon=True).start()

# Основная функция для запуска программы
def main():
    logger.debug("Запуск основной функции")
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
    logger.debug("Запуск значка в трее")
    icon.run()

if __name__ == "__main__":
    main()
