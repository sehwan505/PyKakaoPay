from typing import Pattern
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from fastapi.security import APIKeyCookie
from starlette.responses import Response
from datetime import timedelta
from pykakaopay.single_payment import SinglePayment
from pykakaopay.recurring_payment import RecurringPayment
from pykakaopay.error import ArgumentError, InternalServerError

app = FastAPI()

recurring_cid = "TCSUBSCRIP"
app_admin_key = "7772a592a85bd67d6dd6b1a4634e6231"

reccur_pay = RecurringPayment(app_admin_key, recurring_cid)

cookie_sec = APIKeyCookie(name="session")
cookie_sid = APIKeyCookie(name="sid")


@app.get("/")
async def root(response: Response):
    try:
        partner_order_id = 0  # should change this
        partner_user_id = 0  # should change this too
        res = reccur_pay.ready(
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
    response: Response,
    partner_user_id: str,
    partner_order_id: str,
    pg_token: str,
    tid: str = Depends(cookie_sec),  # approval함수에서 tid를 받아서 사용
):
    """
    If payment is successful
    """
    try:
        res = reccur_pay.approval(tid, partner_order_id, partner_user_id, pg_token)
        response.set_cookie("sid", res["sid"])  # save sid in cookie
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


@app.get("/subscription/")
async def subscribtion(
    sid: str = Depends(cookie_sid),
):
    """
    For additional payment after a set period
    """
    try:
        return reccur_pay.subscription(
            sid,
            0,
            0,
            1,
            10000,
            0,
        )
    except Exception as e:
        return e


@app.get("/inactive/")
async def inactive(
    sid: str = Depends(cookie_sid),
):
    """
    Inactive subscription
    """
    try:
        return reccur_pay.inactive(sid)
    except Exception as e:
        return e


@app.get("/status/")
async def status(
    sid: str = Depends(cookie_sid),
):
    """
    To show status of subscription
    """
    try:
        return reccur_pay.status(sid)
    except Exception as e:
        return e
