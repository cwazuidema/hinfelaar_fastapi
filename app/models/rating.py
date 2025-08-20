from tortoise import fields
from tortoise.models import Model


class Rating(Model):
    """
    Model to store work order session ratings.

    Tracks ratings given for specific work order sessions, allowing users to
    rate their experience or satisfaction with a particular work order.
    """

    id = fields.IntField(pk=True)
    werkboncode = fields.CharField(max_length=100, description="Work order code")
    sessieid = fields.IntField(description="Session ID for the work order")
    value = fields.IntField(description="Rating value (e.g., 1-5 scale)")
    omschrijving = fields.TextField(
        null=True, description="Optional description/comment for the rating"
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "workorder_rating"
        unique_together = (("werkboncode", "sessieid"),)

    def __str__(self) -> str:
        return f"Rating {self.value} for {self.werkboncode} (Session: {self.sessieid})"
