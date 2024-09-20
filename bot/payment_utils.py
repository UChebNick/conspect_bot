import time
import payment, payment_db
import user_db

def main():
    print(88888888888888)
    while True:
        time.sleep(10)

        invoices = payment.get_invoices()['result']
        print(invoices, 0000)

        invoices = invoices['items']
        for invoice in invoices:
            if not payment_db.get_id_by_id(invoice['invoice_id']):
                print(invoice, 77777777)

                try:

                    user_db.add_user_rub(invoice['payload'], invoice['amount'])
                    payment_db.insert(invoice['invoice_id'])
                except:
                    print(f'ошибка: {invoice["payload"]}')