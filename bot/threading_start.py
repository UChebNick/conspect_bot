import threading
from bot.start import bot, msg_utils
from bot.payment_stack import payment_utils

threading.Thread(target=lambda: payment_utils.main()).start()
threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
threading.Thread(target=lambda: msg_utils.main()).start()
