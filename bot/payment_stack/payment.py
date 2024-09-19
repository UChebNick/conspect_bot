from bot.crypto_pay_lib import cryptopaylib


app = cryptopaylib.app(token='249424:AAwHpemeyzG8fhb3McUGOqI1EIiDmc3KK2T')
url = 'https://help.crypt.bot/crypto-pay-api#Invoice'


def create_invoice(rub, user_id):
    return app.create_invoice(rub, currency_type='fiat', fiat='RUB', payload=str(user_id), paid_btn_name='openBot', paid_btn_url=url)


def get_invoices():
    return app.get_invoices(status='paid')

def delete_invoice(id):
    return app.delete_invoice(int(id))


# print(create_invoice(1, 1))
print(get_invoices())