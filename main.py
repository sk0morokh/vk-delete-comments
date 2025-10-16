import os
import re
import requests
import time

# Импорт настроек из отдельного файла
from config import (
    FOLDER_PATH,
    ACCESS_TOKEN,
    VK_API_VERSION,
    DELAY_BETWEEN_REQUESTS,
    DELETE_COMMENT_URL
)

def extract_comment_links_from_file(file_path):
    encodings_to_try = ['cp1251', 'latin1', 'utf-8', 'utf-16']
    content = None

    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
            print(f"✅ {os.path.basename(file_path)} — прочитано ({enc})")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"❌ Ошибка чтения {file_path}: {e}")
            return []

    if not content:
        print(f"❌ Не удалось прочитать файл: {file_path}")
        return []

    urls = re.findall(r'https://vk\.com/wall-?\d+_\d+\?reply=\d+', content)
    print(f"🔎 Найдено ссылок: {len(urls)}")
    return urls

def parse_ids_from_url(url):
    match = re.search(r'wall(-?\d+)_(\d+)\?reply=(\d+)', url)
    if match:
        return {
            'owner_id': int(match.group(1)),
            'comment_id': int(match.group(3))
        }
    return None

def delete_comment(owner_id, comment_id):
    url = DELETE_COMMENT_URL.strip()  # Убираем возможные пробелы
    params = {
        'access_token': ACCESS_TOKEN,
        'v': VK_API_VERSION,
        'owner_id': owner_id,
        'comment_id': comment_id
    }

    try:
        response = requests.post(url, data=params)
        data = response.json()

        if 'response' in data:
            print(f"✅ Успешно удалён: {comment_id}")
            return True
        elif 'error' in data:
            error = data['error']
            code = error['error_code']
            msg = error['error_msg']

            if code == 211:
                print(f"ℹ️ Пропущено {comment_id}: доступ запрещён (стена закрыта/уже удален)")
            elif code == 18:
                print(f"ℹ️ Пропущено {comment_id}: страница удалена или заблокирована")
            elif code == 9:
                print(f"💤 Слишком частые запросы")
                time.sleep(5)
            elif code == 6:
                print(f"💤 Задайте больший интервал между вызовами API")
                time.sleep(1)
            elif code == 14:
                print(f"❌ Требуется ввод кода с картинки (Captcha)")
            elif code == 7:
                print(f"❌ Нет прав на удаление {comment_id}")
            else:
                print(f"❌ [{code}] Ошибка для {comment_id}: {msg}")
            return False
        else:
            print(f"❌ Неизвестный ответ для {comment_id}: {data}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети при удалении {comment_id}: {e}")
        return False
    except Exception as e:
        print(f"❌ Неизвестная ошибка при удалении {comment_id}: {e}")
        return False

def main():
    if not os.path.exists(FOLDER_PATH):
        print(f"❌ Папка не найдена: {FOLDER_PATH}")
        return

    files = [
        os.path.join(FOLDER_PATH, f)
        for f in os.listdir(FOLDER_PATH)
        if f.lower().endswith(('.html', '.htm', '.txt')) and os.path.isfile(os.path.join(FOLDER_PATH, f))
    ]

    if not files:
        print(f"❌ Не найдено ни одного подходящего файла в папке: {FOLDER_PATH}")
        return

    print(f"🔎 Найдено {len(files)} файлов для обработки...\n")

    total_processed = 0
    total_deleted = 0
    processed_comments = set()

    for file_path in files:
        print(f"\nОбработка файла: {os.path.basename(file_path)}")
        urls = extract_comment_links_from_file(file_path)

        for url in urls:
            ids = parse_ids_from_url(url)
            if not ids:
                continue

            comment_id = ids['comment_id']

            if comment_id in processed_comments:
                print(f"ℹ️ Пропущено: {comment_id} (уже обработано)")
                continue

            processed_comments.add(comment_id)
            total_processed += 1

            success = delete_comment(ids['owner_id'], comment_id)
            if success:
                total_deleted += 1

            time.sleep(DELAY_BETWEEN_REQUESTS)

    print("\n" + "="*50)
    print("🔥 Удаление завершено!")
    print(f"📁 Файлов обработано: {len(files)}")
    print(f"🔎 Ссылок найдено: {total_processed}")
    print(f"✅ Успешно удалено: {total_deleted}")
    print(f"❌ Не удалось удалить: {total_processed - total_deleted}")
    print("="*50)


if __name__ == '__main__':
    main()