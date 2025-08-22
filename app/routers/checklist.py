# app/routers/checklist_router.py

from fastapi import APIRouter, Depends
from typing import List

from app.services.checklist_service import ChecklistService

# You can also import Pydantic models for response validation
# from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(
    tags=["Checklist"]
)

# This creates a Pydantic model from your Tortoise model for the response
# AnswerType_Pydantic = pydantic_model_creator(AnswerType)

@router.get(
    "/answer-types", 
    # response_model=List[AnswerType_Pydantic] # Good practice to add this!
)
async def get_all_answer_types(
    service: ChecklistService = Depends(ChecklistService)
):
    """
    Fetches all AnswerType objects from the database.
    """
    return await service.get_all_answer_types()