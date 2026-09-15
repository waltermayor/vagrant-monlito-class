from fastapi import FastAPI

from users import get_user
from orders import get_order
from payments import get_payment


app = FastAPI(title="Monolithic Application")


@app.get("/users/{user_id}")
def user(user_id: int):
    return get_user(user_id)


@app.get("/orders/{order_id}")
def order(order_id: int):
    return get_order(order_id)


@app.get("/payments/{payment_id}")
def payment(payment_id: int):
    return get_payment(payment_id)


@app.get("/health")
def health():
    return {
        "application": "monolith",
        "status": "ok"
    }