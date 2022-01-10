import requests
import json
from pykakaopay.error import ArgumentError, InternalServerError

single_cid = "TC0ONETIME"
recurring_cid = "TCSUBSCRIP"
app_admin_key = "46b46375c1ca60bdef7e97720a32c543"


class Auth:
    def __init__(
        self, app_admin_key: str, cid: str, partner_order_id: str, partner_user_id: str
    ):
        if not (app_admin_key and cid):
            raise ArgumentError("cid or app_admin_key doesn't exist")
        self.app_admin_key = app_admin_key
        self.cid = cid
        self.partner_order_id = partner_order_id
        self.partner_user_id = partner_user_id
        self.redirection_url = None
        self.tid = None
        self.created_at = None

    def _res_check(res):
        ans = json.load(res.text)
        if res.status_code != 200:
            if res.status_code == 400:
                raise ArgumentError(ans["errMsg"])
            if res.status_code == 401:
                raise ArgumentError(ans["errMsg"])
            if res.status_code == 500:
                raise InternalServerError()

    def ready(self, approval_url, cancel_url, fail_url, device: str = "web"):
        url = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization": "KakaoAK " + app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "partner_order_id": self.partner_order_id,
            "partner_user_id": self.partner_user_id,
            "item_name": "연어초밥",
            "quantity": 1,
            "total_amount": 12000,
            "tax_free_amount": 0,
            "vat_amount": 200,
            "approval_url": approval_url,
            "cancel_url": cancel_url,
            "fail_url": fail_url,
        }
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        res_json = res.json()

        self.created_at = res_json["created_at"]
        self.tid = res_json["tid"]
        if device == "mobile_app":
            return res_json["next_redirect_app_url"]
        elif device == "mobile_web":
            return res_json["next_redirect_mobile_url"]
        elif device == "web":
            return res_json["next_redirect_pc_url"]
        elif device == "android_scheme":
            return "android_app_scheme"
        elif device == "ios_scheme":
            return "ios_app_scheme"
        else:
            raise ArgumentError(f"{device} doesn't exist")
