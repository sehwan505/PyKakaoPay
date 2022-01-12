import requests
import json
from pykakaopay.error import ArgumentError, InternalServerError


class Auth:
    def __init__(self, app_admin_key: str, cid: str):
        if not (app_admin_key and cid):
            raise ArgumentError("cid or app_admin_key doesn't exist")
        self.app_admin_key = app_admin_key
        self.cid = cid

    def _res_check(self, res):
        ans = res.text
        if res.status_code != 200:
            if res.status_code == 400:
                raise ArgumentError(ans)
            if res.status_code == 401:
                raise ArgumentError(ans)
            if res.status_code == 500:
                raise InternalServerError()

    def ready(
        self,
        partner_order_id: str,
        partner_user_id: str,
        approval_url: str,
        cancel_url: str,
        fail_url: str,
        item_name: str,
        quantity: int,
        total_amount: int,
        tax_free_amount: int,
        vat_amount: int,
        device: str = "web",
    ):
        url = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization": "KakaoAK " + self.app_admin_key,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": self.cid,
            "partner_order_id": partner_order_id,
            "partner_user_id": partner_user_id,
            "item_name": item_name,
            "quantity": quantity,
            "total_amount": total_amount,
            "tax_free_amount": tax_free_amount,
            "vat_amount": vat_amount,
            "approval_url": approval_url,
            "cancel_url": cancel_url,
            "fail_url": fail_url,
        }
        res = requests.post(url, headers=headers, params=params)
        self._res_check(res)
        res_json = res.json()

        if device == "mobile_app":
            return {
                "redirection_url": res_json["next_redirect_app_url"],
                "tid": res_json["tid"],
                "created_at": res_json["created_at"],
            }
        elif device == "mobile_web":
            return {
                "redirection_url": res_json["next_redirect_mobile_url"],
                "tid": res_json["tid"],
                "created_at": res_json["created_at"],
            }
        elif device == "web":
            return {
                "redirection_url": res_json["next_redirect_pc_url"],
                "tid": res_json["tid"],
                "created_at": res_json["created_at"],
            }
        elif device == "android_scheme":
            return {
                "redirection_url": res_json["android_app_scheme"],
                "tid": res_json["tid"],
                "created_at": res_json["created_at"],
            }
        elif device == "ios_scheme":
            return {
                "redirection_url": res_json["ios_app_scheme"],
                "tid": res_json["tid"],
                "created_at": res_json["created_at"],
            }
        else:
            raise ArgumentError(f"{device} doesn't exist")
