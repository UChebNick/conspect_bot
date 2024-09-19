import speech_recognition as sr
import math
import os

# Максимальная длительность одного аудио фрагмента (в секундах)
MAX_AUDIO_DURATION = 60
r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_adjustment_ratio = 1.5
r.gpu_enabled = True

# Функция для разделения аудио на части
from pydub import AudioSegment
import os

from pydub import AudioSegment
import os


def split_audio_to_minutes(input_file, output_directory):
    """
    Разделяет аудиофайл на части по одной минуте и сохраняет их в указанную директорию.

    Args:
    input_file (str): Путь к исходному аудиофайлу.
    output_directory (str): Путь к директории, где будут сохранены новые файлы.

    Returns:
    list: Список имен сохраненных файлов.
    """
    try:
        # Создаем директорию, если она не существует
        os.makedirs(output_directory, exist_ok=True)

        # Загружаем исходный аудиофайл
        original_audio = AudioSegment.from_file(input_file)

        # Разбиваем аудио на части по минутам
        minute_duration = 10 * 1000  # 60 секунд в минуту, умноженные на 1000 (в миллисекундах)
        file_names = []

        for minute in range(int(len(original_audio) / minute_duration)):
            start_time = minute * minute_duration
            end_time = (minute + 1) * minute_duration
            segment = original_audio[start_time:end_time]

            # Формируем имя файла
            file_name = f"part_{minute + 1}.wav"
            file_path = os.path.join(output_directory, file_name)

            # Сохраняем сегмент в новый файл
            segment.export(file_path, format="wav")
            file_names.append(file_path)

        return file_names

    except (OSError, ValueError) as e:
        print(f"Ошибка при разделении аудиофайла: {e}")
        return []


# Функция для конвертации аудио в текст
def audio_to_text(audio_file):
    try:
        # Открываем аудиофайл
        with sr.AudioFile(audio_file) as source:
            # Записываем аудио
            audio = r.record(source)

        # Распознаем речь
        text = r.recognize_google(audio, language="ru-RU")
        os.remove(audio_file)

        return text



    except sr.UnknownValueError:
        print("Не удалось распознать речь")
        return ""
    except sr.RequestError as e:
        print(f"Ошибка распознавания речи: {e}")
        return ""
