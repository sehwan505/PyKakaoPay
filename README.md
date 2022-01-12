PyKakaoPay
=======

[![Build Status](https://travis-ci.org/sng2c/korail2.svg?branch=master)](https://travis-ci.org/sng2c/korail2)

KakaoPay (https://developers.kakao.com/docs/latest/ko/kakaopay/common) wrapper in Python.

Installing
----------

To install PyKakaoPay, simply:

    $ pip install pykakaopay

Or, you can also install manually:

    $ git clone https://github.com/sehwan505/PyKakaoPay.git
    $ cd PyKakaoPay
    $ python -m poetry install

Using(please check example_ code)
-----

### 1. Auth ###

First, you need to create a Payment object.

```python
>>> from pykakaopay import *
>>> pay = SinglePayment(app_admin_key, single_cid) # to single payment
>>> pay = ReccuringPayment(app_admin_key, recurring_cid) # to reccuring payment
```

### 2. Single payment ###

You can service single payment with `SinglePayment` class.
It has `ready`, `approval`, `cancel`, `order` methods
### ready ###
`ready` method take these arguments:
- partner_order_id: str, order id for payment
- partner_user_id: str, user id who need to pay
- approval_url: str, URL to access when payment is successful
- cancel_url: str, URL to access when payment is canceled
- fail_url: str, URL to access when payment fails
- item_name: str, item name to sell
- quantity: int
- total_amount: int, total amount to be paid
- tax_free_amount: int, tax free amount
- vat_amount: int, vat amount
- device: str = "web", device to be redirected to (web, mobile_app, mobile_web, android_scheme, ios_scheme) 
`ready` returns
- `ready` return redirection_url, tid, created_at
- you should redirect to redirection_url and save tid with session or cookie.

### approval ###

`approval` method take these arguments:
- tid: str
- partner_order_id: str, order id for payment
- partner_user_id: str, user id who need to pay
- pg_token: str, token from approval_url with GET method
- payload: str = None, payload
`approval` returns
- aid: str, 요청 고유 번호
- tid: str, 결제 고유 번호
- cid: str, 가맹점 코드
- sid: str, 정기결제용 ID, 정기결제 CID로 단건결제 요청 시 발급
- partner_order_id: str, 가맹점 주문번호, 최대 100자
- partner_user_id: str, 가맹점 회원 id, 최대 100자
- payment_method_type: str, 결제 수단, CARD 또는 MONEY 중 하나
- amount: Amount, 결제 금액 정보
- card_info: CardInfo, 결제 상세 정보, 결제수단이 카드일 경우만 포함
- item_name: str, 상품 이름, 최대 100자
- item_code: str, 상품 코드, 최대 100자
- quantity: int, 상품 수량
- created_at: Datetime, 결제 준비 요청 시각
- approved_at: Datetime, 결제 승인 시각
- payload: str, 결제 승인 요청에 대해 저장한 값, 요청 시 전달된 내용

### cancel ###
`cancel` method take these arguments:
- tid: str 
- cancel_amount: int, amount to cancel 
- cancel_tax_free_amount: int, tax free amount to cancel
- payload: str, payload
`cancel` returns
- aid: String 요청 고유 번호
- tid: String 결제 고유 번호, 10자
- cid: String 가맹점 코드, 20자
- status: String 결제 상태
- partner_order_id: String 가맹점 주문번호, 최대 100자
- partner_user_id: String 가맹점 회원 id, 최대 100자
- payment_method_type: String 결제 수단, CARD 또는 MONEY 중 하나
- amount Amount: 결제 금액 정보
- approved_cancel_amount: ApprovedCancelAmount 이번 요청으로 취소된 금액
- canceled_amount: CanceledAmount 누계 취소 금액
- cancel_available_amount: CancelAvailableAmount 남은 취소 가능 금액
- item_name: String 상품 이름, 최대 100자
- item_code: String 상품 코드, 최대 100자
- quantity: Integer 상품 수량
- created_at: Datetime 결제 준비 요청 시각
- approved_at: Datetime 결제 승인 시각
- canceled_at: Datetime 결제 취소 시각
- payload: String 취소 요청 시 전달한 값
### order ###
`order` method take these arguments:
- tid, str
`order` returns
tid: String 결제 고유 번호, 20자
cid: String 가맹점 코드
status: String 결제 상태
partner_order_id: String 가맹점 주문번호
partner_user_id: String 가맹점 회원 id
payment_method_type: String 결제 수단, CARD 또는 MONEY 중 하나
amount: Amount 결제 금액
canceled_amount: CanceledAmount 취소된 금액
cancel_available_amount: CanceledAvailableAmount 취소 가능 금액
item_name: String 상품 이름, 최대 100자
item_code: String 상품 코드, 최대 100자
quantity: Integer 상품 수량
created_at: Datetime 결제 준비 요청 시각
approved_at: Datetime 결제 승인 시각
canceled_at: Datetime 결제 취소 시각
selected_card_info: SelectedCardInfo 결제 카드 정보
payment_action_details: PaymentActionDetails[] 결제/취소 상세

Todo
----
1.

License
-------

Source codes are distributed under MIT license.


Author
------

Sehwan Park / [@sehwan-coder](https://github.com/sehwan505)

