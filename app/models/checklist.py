from tortoise import fields
from tortoise.models import Model


class Unit(Model):
    """
    Represents a unit of measurement, e.g., Amperes, Volts.
    """

    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=20, unique=True)
    description = fields.CharField(max_length=255)

    def __str__(self) -> str:
        return self.description


class AnswerType(Model):
    """
    Defines the type of an answer, e.g., Text, List, Value.
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Checklist(Model):
    """
    Represents a checklist containing a set of questions.
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)

    def __str__(self) -> str:
        return self.name


class Question(Model):
    """
    Represents a question in a checklist.
    """

    id = fields.IntField(pk=True)
    checklist = fields.ForeignKeyField(
        "models.Checklist", related_name="questions", on_delete=fields.CASCADE
    )
    text = fields.CharField(max_length=255)
    answer_type = fields.ForeignKeyField(
        "models.AnswerType", related_name="questions", on_delete=fields.RESTRICT
    )
    unit = fields.ForeignKeyField(
        "models.Unit", related_name="questions", null=True, on_delete=fields.SET_NULL
    )
    required = fields.BooleanField(default=False)
    recognition_model = fields.CharField(max_length=50, null=True)
    order = fields.IntField(default=0, min_value=0)

    class Meta:
        ordering = ["order"]
        unique_together = (("checklist", "order"),)

    def __str__(self) -> str:
        return self.text


class ListOption(Model):
    """
    Provides a selectable option for questions of type 'List'.
    """

    id = fields.IntField(pk=True)
    question = fields.ForeignKeyField(
        "models.Question", related_name="options", on_delete=fields.CASCADE
    )
    value = fields.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.question_id} - {self.value}"


class QuestionDependency(Model):
    """
    Defines a dependency between two questions, where answering a parent
    question with a specific list option triggers a child question.
    """

    id = fields.IntField(pk=True)
    parent_question = fields.ForeignKeyField(
        "models.Question", related_name="child_dependencies", on_delete=fields.CASCADE
    )
    trigger_option = fields.ForeignKeyField(
        "models.ListOption", related_name="dependencies", on_delete=fields.CASCADE
    )
    child_question = fields.ForeignKeyField(
        "models.Question", related_name="parent_dependencies", on_delete=fields.CASCADE
    )

    class Meta:
        unique_together = (("parent_question", "trigger_option", "child_question"),)

    def __str__(self) -> str:
        return (
            "If '"
            + str(self.parent_question_id)
            + "' is '"
            + str(self.trigger_option_id)
            + "', then show '"
            + str(self.child_question_id)
            + "'"
        )


class ChecklistResponse(Model):
    """
    Represents a complete response to a checklist, including all answers and metadata.
    """

    id = fields.IntField(pk=True)
    checklist = fields.ForeignKeyField(
        "models.Checklist", related_name="responses", on_delete=fields.CASCADE
    )
    workordernumber = fields.CharField(max_length=50)
    bag = fields.CharField(max_length=50)
    answers = fields.JSONField(default=dict)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = (("checklist", "workordernumber", "bag", "answers"),)

    def __str__(self) -> str:
        return f"Response to {self.checklist_id} - {self.workordernumber}"
