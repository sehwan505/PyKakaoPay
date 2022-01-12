import requests
from pykakaopay.auth import Auth


class SinglePayment(Auth):
    def __init__(self, app_admin_key: str, cid: str):
        super().__init__(app_admin_key, cid)

    def approval(
        self,
        tid: str,
        partner_order_id: str,
        partner_user_id: str,
        pg_token: str,
        payload: str = None,
    ):
        url = "https://kapi.kakao.com/v1/payment/approve"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "tid": tid,
            "partner_order_id": partner_order_id,
            "partner_user_id": partner_user_id,
            "pg_token": pg_token,
            "payload": payload,
        }
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        return res.json()

    def cancel(
        self, tid: str, cancel_amount: int, cancel_tax_free_amount: int, payload: str
    ):
        url = "https://kapi.kakao.com/v1/payment/cancel"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "tid": tid,
            "cancel_amount": cancel_amount,
            "cancel_tax_free_amount": cancel_tax_free_amount,
            "payload": payload,
        }

        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        if res.json()["status"] == "QUIT_PAYMENT":
            return res.json()

    def order(self, tid: str):
        url = "https://kapi.kakao.com/v1/payment/order"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "tid": tid,
        }

        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        return res.json()
