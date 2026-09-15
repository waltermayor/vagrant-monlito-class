from fastapi import HTTPException

users = {
    1: {
        "id": 1,
        "name": "Walter",
        "email": "walter@example.com"
    },
    2: {
        "id": 2,
        "name": "Maria",
        "email": "maria@example.com"
    }
}


def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]