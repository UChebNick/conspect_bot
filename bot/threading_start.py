import threading
import bot, msg_utils
import payment_utils

threading.Thread(target=lambda: payment_utils.main()).start()
threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
threading.Thread(target=lambda: msg_utils.main()).start()
