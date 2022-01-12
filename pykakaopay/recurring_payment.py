import requests
from pykakaopay.auth import Auth


class RecurringPayment(Auth):
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

    def subscription(
        self,
        sid: str,
        partner_order_id: str,
        partner_user_id: str,
        quantity: int,
        total_amount: int,
        tax_free_amount: int,
    ):
        url = "https://kapi.kakao.com/v1/payment/subscription"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "sid": sid,
            "partner_order_id": partner_order_id,
            "partner_user_id": partner_user_id,
            "quantity": quantity,
            "total_amount": total_amount,
            "tax_free_amount": tax_free_amount,
        }
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        return res.json()

    def inactive(self, sid: str):
        url = "https://kapi.kakao.com/v1/payment/manage/subscription/inactive"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {"cid": self.cid, "sid": sid}
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        return res.json()

    def status(self, sid: str):
        url = "https://kapi.kakao.com/v1/payment/manage/subscription/status"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {"cid": self.cid, "sid": sid}
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        return res.json()
