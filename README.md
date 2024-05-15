# через терминал windows:
# перейдите в корень проекта при помощи команд cd имя каталога...   вплоть до целевого. подсказка (ls)

# содержимое файла HIDDEN/config.py:
BINANCE_API_PUBLIC_KEY = "сюда вставте your public binance api key"
BINANCE_API_PRIVATE_KEY = "сюда вставте your private binance api key"
# Важно! При генерации апи ключей в вашем бинанс приложении нужно выставить метку для торговли на фьючерсах, а также снять метку ограничений по ip локации --- ВАЖНО!
# через официальный Bot Father (https://web.telegram.org/k/#@BotFather) создайте в tg своего бота, скопируйте токен и перейдите по ссылке в бота
TG_TOKEN = "сюда вставте секретный телеграм токен бота" # Denis ema tg bot token
COIN_MARKET_CUP_TOKEN = "15dc358f-b26f-4200-8ee9-7f60b143480a" # -- это ключ апи COIN_MARKET_CUP разработчика. Пользуйтесь наздоровье! 
ACESS_TOKEN = "dd" # -- ваш кастомный ключ доступа в ваш тг бот. можно изменить на любой
#///////////////////

# возможно придется обновить установщик пакетов:
# python -m pip install --upgrade pip

# установка зависимостей:
# pip install numpy pandas pandas-ta pyTelegramBotAPI requests
# //////////////////////
# исполнительная команда:
# python main.py
# в принт должно вывести следующее сообщение: 'Пожалуйста перейдите в интерфейс вашего телеграм бота!'
# завершить работу: Ctrl + Z


# //////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////


# через терминал linux:
# обновляем дистрибутив линукс:
# sudo apt update -- всегда при установках подобного рода

# С этим ОСТОРОЖНО, только при наличии активного виртуального окружения (обновление установщика пакетов python)!!
# pip install --upgrade pip -- пропустить. Но команду знать нужно
# /////////////////////////////////////

# перейдите в корень проекта при помощи команд cd имя каталога...   вплоть до целевого. подсказка (ls)

# создаем пустой файл где будем прятать ключи:
# touch .env
# Введите команду nano .env и нажмите клавишу Enter. Если файл .env уже существует, он будет открыт для редактирования. Если файл не существует, Nano создаст новый файл с этим именем.
# Теперь вы находитесь в редакторе Nano и можете ввести текст в файл.
# Введите нужный текст в файл.
#///////////////////
# при помощи команды Ctrl + Shift + V вставте ранее скопированное содержание текста в редактор
# содержимое файла .env:
BINANCE_API_PUBLIC_KEY = "сюда вставте your public binance api key"
BINANCE_API_PRIVATE_KEY = "сюда вставте your private binance api key"
# Важно! При генерации апи ключей в вашем бинанс приложении нужно выставить метку для торговли на фьючерсах, а также снять метку ограничений по ip локации --- ВАЖНО!
# через официальный Bot Father создайте в tg своего бота, скопируйте токен и перейдите по ссылке в бота
TG_TOKEN = "сюда вставте секретный телеграм токен бота" # Denis ema tg bot token
COIN_MARKET_CUP_TOKEN = "15dc358f-b26f-4200-8ee9-7f60b143480a" # -- это ключ апи COIN_MARKET_CUP разработчика. Пользуйтесь наздоровье! 
ACESS_TOKEN = "d100" # -- ваш кастомный ключ доступа в ваш тг бот. можно изменить на любой
#///////////////////
# Чтобы сохранить внесенные изменения, нажмите Ctrl + O (это буква "O", не ноль). В нижней части окна редактора вы увидите запрос "Save file as" (Сохранить файл как). Нажмите клавишу Enter, чтобы подтвердить сохранение файла.
# Затем, чтобы выйти из редактора Nano, нажмите Ctrl + X.
# Готово! Теперь ваш файл .env должен содержать введенный вами текст.
#////////////////////////////////////////////////////

# можно попробовать пропустить....
# установка виртуального окружения
# sudo apt install python3-venv
# python3 -m venv .venv
# активация виртуального окружения
# source .venv/bin/activate
#///////////////////////////////

# установка зависимостей:
# pip install -r requirements.txt -- установка пакетов
# //////////////////////
# исполнительная команда:
# python main.py
# в принт должно вывести следующее сообщение: 'Пожалуйста перейдите в интерфейс вашего телеграм бота!'

# завершить работу: Ctrl + Z
# убить фоновые потоки: killall -9 python
