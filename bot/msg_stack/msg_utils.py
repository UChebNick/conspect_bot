import json
import os
import time

from bot.msg_stack import audio2text_stack_db as stack
from bot import audio_to_text
from bot import gpt
from bot import user_db
from bot import utils
import datetime
from bot.loader import token
from bot.loader import audio_path

def main():
    while True:
        utils.delete_files_in_folder(audio_path)
        for row in stack.select_data():
            print(row)
            time.sleep(5)
            try:
                if user_db.get_user(row[5])[1] < 0:
                    continue
                time.sleep(0.1)
                print(row)
                res = []
                split_audio = audio_to_text.split_audio_to_minutes(input_file=row[2], output_directory='audio')
                for a in split_audio:
                    res.append(audio_to_text.audio_to_text(a))
                if row[3]:
                    links = [f'https://api.telegram.org/bot{token}/getFile?file_id={file_id}' for file_id in json.loads(row[3])]
                else:
                    links = None
                text = ' '.join(res)
                user_rubs = user_db.get_user(row[5])[1]
                req_rubs = utils.tokens2rub(row[6], len(f'составь конспект по тексту с моей лекции - "{text}" {row[4]}'.split()), True)
                if user_rubs - req_rubs <= 0:
                    id = stack.insert_data(datetime.datetime.now().timestamp(), None, None, row[5], None,
                                           status=5)
                else:
                    max_tokens = utils.rub2tokens(row[6], user_rubs - req_rubs, False)
                    response = gpt.send_request(links, text, row[4], row[6], max_tokens)
                    response_text = response['choices'][0]['message']['content']
                    rubs = utils.tokens2rub(row[6], response['usage']['prompt_tokens'], True) + utils.tokens2rub(row[6], response['usage']['completion_tokens'], False)
                    id = stack.insert_data(datetime.datetime.now().timestamp(), None, response_text, row[5], None, status=3)
                    stack.update_status(row[0], 4)
                    print(id)
                    user_db.add_user_rub(row[5], - rubs)
            except Exception as e:
                print(e)

