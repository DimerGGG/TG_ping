Server Status Monitor Bot
This is a Python program that monitors the status of a server by periodically pinging its IP address. It sends notifications to a Telegram bot when the server's status changes. The program runs in the system tray and minimizes the console window upon startup.

Requirements
Python 3.x
ping3
telebot
pystray
Pillow
pywin32
configobj
Installation
Install the required libraries:

pip install ping3 telebot pystray pillow pywin32 configobj
Create a config.ini file in the same directory as the script with the following content:

ini
[DEFAULT]
BOT_TOKEN = <your-telegram-bot-token>
IP_ADRESS = <server-ip-address>
AWAIT = <interval-in-seconds>
ID = <your-telegram-chat-id>
Usage
Run the script:

python your_script.py
The program will minimize the console window and run in the system tray. You can exit the program by right-clicking the tray icon and selecting "Exit".

Compiling to EXE
Install PyInstaller:

pip install pyinstaller
Compile the script:

pyinstaller --onefile --noconsole your_script.py
Run the generated your_script.exe file. The program will start minimized in the system tray.

Notes
Ensure that the bot token and chat ID are correctly set in the config.ini file.
The program sends a notification to the specified Telegram chat whenever the server's status changes.


_____________________________________________________________________________________________________
Бот для мониторинга статуса сервера
Это программа на Python, которая отслеживает статус сервера, периодически пингуя его IP-адрес. Она отправляет уведомления в Telegram-бота при изменении статуса сервера. Программа работает в системном трее и сворачивает окно консоли при запуске.

Требования
Python 3.x
ping3
telebot
pystray
Pillow
pywin32
configobj
Установка
Установите необходимые библиотеки:

pip install ping3 telebot pystray pillow pywin32 configobj
Создайте файл config.ini в той же директории, что и скрипт, со следующим содержанием:

ini
[DEFAULT]
BOT_TOKEN = <токен-вашего-telegram-бота>
IP_ADRESS = <ip-адрес-сервера>
AWAIT = <интервал-в-секундах>
ID = <id-вашего-telegram-чата>
Использование
Запустите скрипт:


python your_script.py
Программа свернет окно консоли и будет работать в системном трее. Вы можете выйти из программы, щелкнув правой кнопкой мыши по значку в трее и выбрав "Exit".

Компиляция в EXE
Установите PyInstaller:

pip install pyinstaller
Скомпилируйте скрипт:

pyinstaller --onefile --noconsole your_script.py
Запустите сгенерированный файл tg_bot_3.py. Программа начнет работу, будучи свернутой в системный трей.

Заметки
Убедитесь, что токен бота и ID чата правильно указаны в файле config.ini.
Программа отправляет уведомление в указанный Telegram-чат всякий раз, когда статус сервера изменяется.
