import soundfile as sf   #   pip install pysoundfile
import os

def save_voice(bot, message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(f"{message.message_id}.{message.voice.mime_type.split('/')[-1].split('+')[-1]}", "wb") as f:
        f.write(downloaded_file)
        f.close()

    # Конвертируем аудио в WAV формат
    data, samplerate = sf.read(fr"{message.message_id}.{message.voice.mime_type.split('/')[-1].split('+')[-1]}")
    os.remove(fr"{message.message_id}.{message.voice.mime_type.split('/')[-1].split('+')[-1]}")
    sf.write(fr"D:\conspect_bot\bot\audio\{message.message_id}.wav", data, samplerate)
    return fr"D:\conspect_bot\bot\audio\{message.message_id}.wav"

def tokens2rub(gpt, tokens, req):
    if gpt == 'gpt-3.5-turbo-1106':
        r = 0.3 if req else 0.6
    elif gpt == 'gpt-3.5-turbo-0125':
        r = 0.144 if req else 0.432
    elif gpt == 'gpt-4':
        r = 8.64 if req else 17.28
    elif gpt == 'gpt-4-turbo':
        r = 2.88 if req else 8.64
    elif gpt == 'o1-preview':
        r = 3.0 if req else 9.0
    elif gpt == 'o1-mini':
        r = 0.864 if req else 1.8
    elif gpt == 'gpt-4o':
        r = 1.44 if req else 4.32
    elif gpt == 'gpt-4o-2024-08-06':
        r = 0.72 if req else 2.88
    elif gpt == 'gpt-4o-mini':
        r = 0.0432 if req else 0.1728
    else:
        return None # Возвращаем None, если не найден соответствующий тариф

    return tokens * r / 1000

def rub2tokens(gpt, rub, req):
    if gpt == 'gpt-3.5-turbo-1106':
        r = 0.3 if req else 0.6
    elif gpt == 'gpt-3.5-turbo-0125':
        r = 0.144 if req else 0.432
    elif gpt == 'gpt-4':
        r = 8.64 if req else 17.28
    elif gpt == 'gpt-4-turbo':
        r = 2.88 if req else 8.64
    elif gpt == 'o1-preview':
        r = 3.0 if req else 9.0
    elif gpt == 'o1-mini':
        r = 0.864 if req else 1.8
    elif gpt == 'gpt-4o':
        r = 1.44 if req else 4.32
    elif gpt == 'gpt-4o-2024-08-06':
        r = 0.72 if req else 2.88
    elif gpt == 'gpt-4o-mini':
        r = 0.0432 if req else 0.1728
    else:
        return None  # Возвращаем None, если не найден соответствующий тариф

    if r == 0:
        return None  # Возвращаем None, если стоимость за токен равна 0

    return rub / r * 1000


def delete_files_in_folder(folder_path):
    """
    Удаляет все файлы в указанной папке.

    Args:
        folder_path (str): Путь к папке, в которой нужно удалить все файлы.
    """
    # Проверяем, существует ли папка
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Перебираем все файлы в папке
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Проверяем, что это файл, а не папка
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Файл '{filename}' успешно удален.")
                except OSError as e:
                    print(f"Не удалось удалить файл '{filename}': {e}")
    else:
        print(f"Папка '{folder_path}' не существует или недоступна.")
