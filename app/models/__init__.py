from typing import Dict, Any


# NOTE: We hardcode the database credentials for now. We'll switch to environment variables later.
DATABASE_URL: str = (
    "postgres://hinfelaar_fastapi_db_user:hinfelaar_fastapi_db_password@localhost:5432/hinfelaar_fastapi"
)


# Tortoise ORM configuration used by the app and by Aerich.
# Aerich command will reference this via `-t app.models.TORTOISE_ORM`.
TORTOISE_ORM: Dict[str, Any] = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            # Include your app's models here, plus `aerich.models` for migrations
            "models": [
                "app.models.user",
                "app.models.checklist",
                "app.models.rating",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
