# app/schemas/syntess.py
from pydantic import BaseModel, Field

class SyntessWorkOrder(BaseModel):
    SES_ACT_UITVBEST_GC_ID: int | None = None
    PRO_GC_ID: int | None = None
    DOC_GC_ID: int | None = None
    ADRES_POSTCODE: str | None = None
    ADRES_HUIS_NR: str | None = None
    ADRES_HUIS_NR_TOEVOEGING: str | None = None

class WorkOrderDTO(BaseModel):
    uitvoerbestekId: int = 0
    projectId: int = 0
    documentId: int = 0
    postalCode: str = ""
    houseNumber: str = ""
    addition: str = ""