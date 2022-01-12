from typing import Pattern
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from fastapi.security import APIKeyCookie
from starlette.responses import Response
from datetime import timedelta
from pykakaopay.single_payment import SinglePayment
from pykakaopay.error import ArgumentError, InternalServerError

app = FastAPI()

single_cid = "TC0ONETIME"
app_admin_key = "7772a592a85bd67d6dd6b1a4634e6231"

pay = SinglePayment(app_admin_key, single_cid)

cookie_sec = APIKeyCookie(name="session")


@app.get("/")
async def root(response: Response):
    try:
        partner_order_id = 0 #should change this
        partner_user_id = 0 #should change this too
        res = pay.ready(
            partner_order_id,
            partner_user_id,
            f"http://127.0.0.1:8000/success/{partner_order_id}/{partner_user_id}",
            f"http://127.0.0.1:8000/cancel/{partner_order_id}/{partner_user_id}",
            f"http://127.0.0.1:8000/fail/{partner_order_id}/{partner_user_id}",
            "수박",
            1,  # quantity
            10000,  # total_amount
            0,  # tax_free_amount
            800,  # vat_amount
            "web",
        )
        response.set_cookie("session", res["tid"])  # save tid in cookie
        return {"message": res}
    except Exception as e:
        return e


@app.get("/success/{partner_order_id}/{partner_user_id}")
async def approval(
    partner_user_id: str,
    partner_order_id: str,
    pg_token: str,
    tid: str = Depends(cookie_sec),  # approval함수에서 tid를 받아서 사용
):
    """
    If payment is successful
    """
    try:
        return pay.approval(tid, partner_order_id, partner_user_id, pg_token)
    except Exception as e:
        return e


@app.get("/cancel/{partner_order_id}/{partner_user_id}")
async def cancel(
    partner_user_id: str,
    partner_order_id: str,
    tid: str = Depends(cookie_sec),
):
    """
    If payment is canceled during process
    """
    return 0


@app.get("/fail/{partner_order_id}/{partner_user_id}")
async def fail(
    partner_user_id: str,
    partner_order_id: str,
    tid: str = Depends(cookie_sec),
):
    """
    If payment fails
    """
    return 0


async def payment_cancel(tid: str = Depends(cookie_sec)):
    """
    Cancel payment after process
    """
    return pay.cancel(tid, 1000, 0, "payload")
