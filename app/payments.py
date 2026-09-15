from fastapi import HTTPException
from .orders import get_order


payments = {
    1: {
        "id": 1,
        "order_id": 1,
        "status": "paid",
        "amount": 1500
    },
    2: {
        "id": 2,
        "order_id": 2,
        "status": "pending",
        "amount": 100
    }
}


def get_payment(payment_id: int):

    if payment_id not in payments:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payment = payments[payment_id]

    order = get_order(payment["order_id"])

    return {
        "payment": payment,
        "order": order
    }