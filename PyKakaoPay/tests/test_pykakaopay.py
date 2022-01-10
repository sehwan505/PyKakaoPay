from pykakaopay import __version__
from pykakaopay.single_payment import SinglePayment

single_cid = "TC0ONETIME"
recurring_cid = "TCSUBSCRIP"
app_admin_key = "7772a592a85bd67d6dd6b1a4634e6231"


def test_version():
    assert __version__ == "0.1.0"


def test_single_payment():
    pay = SinglePayment(app_admin_key, single_cid, "1", "1")
    res = pay.ready(
            "http://127.0.0.1:8000/success/",
            "http://127.0.0.1:8000/cancel/",
            "http://127.0.0.1:8000/fail/",
            "web",
        )
    assert res == "ABC"