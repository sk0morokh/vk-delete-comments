# Массовое удаление своих комментариев из ВКонтакте

Этот скрипт позволяет автоматически удалять ваши комментарии под записями на стенах в сообществах и профилях ВКонтакте, используя данные из скачанного архива активности

## 🔧 Функционал

Скрипт:
- Сканирует HTML/HTM/TXT-файлы из папки с архивом ВК.
- Извлекает ссылки на ваши комментарии (вида `https://vk.com/wall-12345_12345?reply=111213`).
- Парсит `owner_id` и `comment_id`.
- Отправляет запросы на удаление через VK API.
- Обрабатывает ошибки (ограничения, частые запросы и т.д.).
- Поддерживает разные кодировки файлов (UTF-8, CP1251 и др.).

---

## 📦 Требования

- Python 3.7+
- Библиотеки: `requests`

Установка зависимостей:
```bash
pip install requests
```

## ⚙️ Настройка
### 1. Скачайте архив данных ВК

Перейдите в настройки [приватности](https://vk.com/data_protection?spm=a2ty_o01.29997173.0.0.6454c921cOKv6M&section=rules&scroll_to_archive=1)  → «Запросить копию моих данных» → выберите «Архив активности» → скачайте ZIP-файл после готовности.

<img width="452" height="210" alt="image" src="https://github.com/user-attachments/assets/9f49949f-2e4b-4d13-9d2f-92d5ddb74f7d" />


### 2. Извлеките папку comments
Найдите в архиве папку comments (обычно содержит .html, .htm или .txt файлы).

<img width="646" height="432" alt="image" src="https://github.com/user-attachments/assets/bd8e9179-e9d8-42e3-ab29-a0a87029f5c1" />


### 3. Настройте config.py
```
FOLDER_PATH = r'Z:/Архив_ВК/comments/' # Путь к папке с файлами https://vk.com/data_protection?section=rules&scroll_to_archive=1
ACCESS_TOKEN = 'vk1.a.Sq1MjQsdfsdffffdsfsfsdfsdf'  # Токен через f12
VK_API_VERSION = '5.199' # Версия VK API https://dev.vk.com/ru/reference/versions
DELAY_BETWEEN_REQUESTS = 0.05 # Задержка между запросами к API (в секундах)
DELETE_COMMENT_URL = 'https://api.vk.com/method/wall.deleteComment' # Версия VK API https://dev.vk.com/ru/method/board.deleteComment
```

### 4. Получите токен доступа
- Откройте VK и войдите в свой аккаунт.
- Нажмите F12 → вкладка Network (Сеть) → перезагрузите страницу.
- Найдите любой запрос к api.vk.com, кликните по нему.
- В параметрах запроса найдите access_token=... — это ваш токен.
- Скопируйте в config.py (начинается с vk1.a.).
<img width="799" height="342" alt="image" src="https://github.com/user-attachments/assets/b7298105-00c3-46ae-a3cf-71046ee11aa1" />

**🔥 ВАЖНО, такой токен протухает в среднем каждые 5 минут и каждый раз нужно обновлять страницу в браузере для получения нового токена, так что удаление может затянуться!**

## 🔐 Никогда не передавайте и не публикуйте свой токен! 
