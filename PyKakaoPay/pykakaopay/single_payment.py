import requests
import json
from pykakaopay.error import ArgumentError, InternalServerError
from pykakaopay.auth import Auth


class SinglePayment(Auth):
    def __init__(
        self, app_admin_key: str, cid: str, partner_order_id: str, partner_user_id: str
    ):
        super().__init__(app_admin_key, cid, partner_order_id, partner_user_id)

    def approval(self, pg_token: str, payload: str):
        url = "https://kapi.kakao.com/v1/payment/approve"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "tid": self.tid,
            "partner_order_id": self.partner_order_id,
            "partner_user_id": self.partner_user_id,
            "pg_token": pg_token,
            "payload": payload,
        }
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        return res.json()

    def cancel(self, cancel_amount: int, cancel_tax_free_amount: int, payload: str):
        url = "https://kapi.kakao.com/v1/payment/cancel"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "tid": self.tid,
            "cancel_amount": cancel_amount,
            "cancel_tax_free_amount": cancel_tax_free_amount,
            "payload": payload,
        }

        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        if res.json()["status"] == "QUIT_PAYMENT":
            return res.json()


def cancel(
    app_admin_key: str,
    cid: str,
    tid: str,
    cancel_amount: int,
    cancel_tax_free_amount: int,
    payload: str,
):
    url = "https://kapi.kakao.com/v1/payment/cancel"
    headers = {
        "Authorization": "KakaoAK " + app_admin_key,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": cid,
        "tid": tid,
        "cancel_amount": cancel_amount,
        "cancel_tax_free_amount": cancel_tax_free_amount,
        "payload": payload,
    }

    res = requests.post(url, headers=headers, params=params)
    ans = json.load(res.text)
    if res.status_code != 200:
        if res.status_code == 400:
            raise ArgumentError(ans["errMsg"])
        if res.status_code == 401:
            raise ArgumentError(ans["errMsg"])
        if res.status_code == 500:
            raise InternalServerError()
    if res.json()["status"] == "QUIT_PAYMENT":
        return res.json()


def order(app_admin_key: str, cid: str, tid: str):
    url = "https://kapi.kakao.com/v1/payment/order"
    headers = {
        "Authorization": "KakaoAK " + app_admin_key,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": cid,
        "tid": tid,
    }

    res = requests.post(url, headers=headers, params=params)
    ans = json.load(res.text)
    if res.status_code != 200:
        if res.status_code == 400:
            raise ArgumentError(ans["errMsg"])
        if res.status_code == 401:
            raise ArgumentError(ans["errMsg"])
        if res.status_code == 500:
            raise InternalServerError()

    return res.json()
