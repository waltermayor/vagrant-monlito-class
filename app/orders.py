from fastapi import HTTPException
from .users import get_user


orders = {
    1: {
        "id": 1,
        "user_id": 1,
        "product": "Laptop",
        "amount": 1500
    },
    2: {
        "id": 2,
        "user_id": 2,
        "product": "Keyboard",
        "amount": 100
    }
}


def get_order(order_id: int):

    if order_id not in orders:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order = orders[order_id]

    user = get_user(order["user_id"])

    return {
        "order": order,
        "user": user
    }