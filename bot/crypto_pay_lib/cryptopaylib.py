import httpx
import string
import random

def generate_random_string(length=64):
    # Диапазон UTF-8 символов, который будет использоваться
    charset = string.ascii_letters + string.digits + ''.join(chr(i) for i in range(0x4e00, 0x9fff))

    # Генерация случайной строки
    return ''.join(random.choice(charset) for _ in range(length))


class app:
    def __init__(self, token, url='https://pay.crypt.bot/api'):
        self.token = token
        self.url = url

    def get_me(self):
        return httpx.get(url=self.url + '/getMe', headers={'Crypto-Pay-API-Token': self.token}).json()

    def create_invoice(self, amount: str, currency_type: str = None, asset: str = None, fiat: str = None, accepted_assets: str = None, description: str = None, hidden_message: str = None, paid_btn_name: str = None, paid_btn_url: str = None, payload: str = None, allow_comments: bool = None, allow_anonymous: bool = None, expires_in: int = None):
        params = {
            'amount': amount,
            'currency_type': currency_type,
            'asset': asset,
            'fiat': fiat,
            'accepted_assets': accepted_assets,
            'description': description,
            'hidden_message': hidden_message,
            'paid_btn_name': paid_btn_name,
            'paid_btn_url': paid_btn_url,
            'payload': payload,
            'allow_comments': allow_comments,
            'allow_anonymous': allow_anonymous,
            'expires_in': expires_in
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/createInvoice', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def delete_invoice(self, invoice_id: int):
        params = {
            'invoice_id': invoice_id
        }

        return httpx.get(url=self.url + '/deleteInvoice', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def create_check(self, asset: str, amount: str, pin_to_user_id: int = None, pin_to_username: int = None):
        params = {
            'asset': asset,
            'amount': amount,
            'pin_to_user_id': pin_to_user_id,
            'pin_to_username': pin_to_username
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/createCheck', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def delete_check(self, check_id: int):
        params = {
            'check_id': check_id
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/deleteCheck', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def transfer(self, user_id: int, asset: str, amount: str, spend_id:str = generate_random_string(), comment: str = None, disable_send_notification: bool = None):
        params = {
            'user_id': user_id,
            'asset': asset,
            'amount': amount,
            'spend_id': spend_id,
            'comment': comment,
            'disable_send_notification': disable_send_notification
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/transfer', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_invoices(self, asset: str = None, fiat: str = None, invoice_ids: str = None, status: str = None, offset: int = None, count: int = None):
        params = {
            'asset': asset,
            'fiat': fiat,
            'invoice_ids': invoice_ids,
            'status': status,
            'offset': offset,
            'count': count
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/getInvoices', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_transfers(self, asset: str = None, transfer_ids: str = None, offset: int = None, count: int = None):
        params = {
            'asset': asset,
            'transfer_ids': transfer_ids,
            'offset': offset,
            'count': count
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/getTransfers', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_checks(self, asset: str = None, check_ids: str = None, offset: int = None, count: int = None):
        params = {
            'asset': asset,
            'transfer_ids': check_ids,
            'offset': offset,
            'count': count
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/getChecks', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_balance(self):
        return httpx.get(url=self.url + '/getBalance', headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_exchange_rates(self):
        return httpx.get(url=self.url + '/getExchangeRates', headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_currencies(self):
        return httpx.get(url=self.url + '/getCurrencies', headers={'Crypto-Pay-API-Token': self.token}).json()

    def get_stats(self, start_at: str = None, end_at: str = None):
        params = {
            'start_at': start_at,
            'end_at': end_at
        }

        params = {k: v for k, v in params.items() if v is not None}

        return httpx.get(url=self.url + '/getStats', params=params, headers={'Crypto-Pay-API-Token': self.token}).json()
