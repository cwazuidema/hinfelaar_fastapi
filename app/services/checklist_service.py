# app/services/checklist_service.py

from typing import List
from app.models.checklist import AnswerType

class ChecklistService:
    async def get_all_answer_types(self) -> List[AnswerType]:
        """
        Business logic to retrieve all AnswerType objects.
        
        This is where you would add any additional logic,
        like filtering, sorting, or permission checks in the future.
        """
        # This is it. This is the clean, one-liner you were looking for.
        # It's identical in spirit to Django's AnswerType.objects.all()
        return await AnswerType.all()