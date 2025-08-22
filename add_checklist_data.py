import asyncio
from typing import Any, Dict, List, Optional

from tortoise import Tortoise

from app.models import TORTOISE_ORM
from app.models.checklist import (
    Unit,
    AnswerType,
    Checklist,
    Question,
    ListOption,
    QuestionDependency,
)


# This data mirrors the Django management command structure provided.
DATA: Dict[str, Any] = {
    "units": [
        {"code": "A", "description": "Amperes"},
        {"code": "V", "description": "Volts"},
        {"code": "Ohm", "description": "Ohms"},
        {"code": "s", "description": "Seconds"},
        {"code": "mA", "description": "Milliamperes"},
        {"code": "ms", "description": "Milliseconds"},
        {"code": "year", "description": "Year"},
        {"code": "st", "description": "Stuks"},
    ],
    "answer_types": [
        {"name": "Text"},
        {"name": "Number"},
        {"name": "List"},
        {"name": "External Document"},
        {"name": "Image Recognition"},
        {"name": "Header"},
        {"name": "Signature"},
    ],
    "checklists": [
        {
            "name": "Checklist (Bewoners)",
            "description": "Een checklist voor de bewoners",
            "questions": [
                {
                    "text": "Foto van de groepenkast",
                    "answer_type": "Image Recognition",
                    "recognition_model": "groepenkast",
                    "required": True,
                    "order": 1,
                },
                {
                    "text": "Groepenverklaring aanwezig",
                    "answer_type": "External Document",
                    "required": True,
                    "order": 2,
                },
                {
                    "text": "Groepenkast of verdeelinrichting is gecontroleerd en in orde bevonden",
                    "answer_type": "List",
                    "required": True,
                    "order": 3,
                    "options": [{"value": "Ja"}, {"value": "Nee"}],
                },
                {
                    "text": "Schakelmateriaal gecontroleerd en in orde bevonden?",
                    "answer_type": "List",
                    "required": True,
                    "order": 4,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee (artikel +arbeid in de oplossingen)"},
                    ],
                },
                {
                    "text": "Zichtbare aardingen in badkamer(s) CV-leidingen en in meterkast in orde",
                    "answer_type": "List",
                    "required": True,
                    "order": 5,
                    "options": [{"value": "Ja"}, {"value": "Nee"}],
                },
                {
                    "text": "Foto van het afkeurpunt",
                    "answer_type": "External Document",
                    "required": False,
                    "order": 6,
                },
                {
                    "text": "Rookmelders aangetroffen en houdbaarheid gecontroleerd?",
                    "answer_type": "List",
                    "required": True,
                    "order": 17,
                    "options": [{"value": "Ja"}, {"value": "Nee"}],
                },
                {
                    "text": "Rookmelder houdbaar tot welk jaartal",
                    "answer_type": "External Document",
                    "unit": "year",
                    "required": True,
                    "order": 18,
                },
                {
                    "text": "Soort rookmelder?",
                    "answer_type": "List",
                    "required": True,
                    "order": 19,
                    "options": [{"value": "230 volt"}, {"value": "Batterij gevoed"}],
                },
                {
                    "text": "Aantal rookmelders",
                    "answer_type": "List",
                    "required": False,
                    "order": 20,
                    "options": [
                        {"value": "1"},
                        {"value": "2"},
                        {"value": "3"},
                        {"value": "4"},
                        {"value": "5"},
                        {"value": "6"},
                        {"value": "7"},
                        {"value": "8"},
                        {"value": "9"},
                        {"value": "10"},
                    ],
                },
                {
                    "text": "Bevindingen doorgenomen met de bewoner?",
                    "answer_type": "List",
                    "required": True,
                    "order": 21,
                    "options": [{"value": "Ja"}, {"value": "Nee"}],
                },
                {
                    "text": "Naam uitvoerende servicemonteur",
                    "answer_type": "Text",
                    "required": True,
                    "order": 22,
                },
                {
                    "text": "Handtekening servicemonteur",
                    "answer_type": "Signature",
                    "required": True,
                    "order": 23,
                },
            ],
            "dependencies": [
                {
                    "parent_question_order": 5,
                    "trigger_value": "Nee",
                    "child_question_order": 6,
                }
            ],
        },
        {
            "name": "Checklist (complex)",
            "description": "Een checklist voor complexen",
            "questions": [
                {
                    "text": "Nood- of vluchtwegsinstallatie aanwezig?",
                    "answer_type": "List",
                    "required": True,
                    "order": 1,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Wordt deze jaarlijks geinspecteerd?",
                    "answer_type": "List",
                    "required": False,
                    "order": 2,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Aantal nood-vlucht weg armaturen?",
                    "answer_type": "Number",
                    "required": False,
                    "order": 3,
                    "unit": "st",
                },
                {
                    "text": "Algemene Brandmeldinstallatie?",
                    "answer_type": "List",
                    "required": True,
                    "order": 4,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Wordt deze jaarlijks geinspecteerd?",
                    "answer_type": "List",
                    "required": False,
                    "order": 5,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Elektrische deurdranger of speedgate aanwezig?",
                    "answer_type": "List",
                    "required": True,
                    "order": 6,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Wordt deze jaarlijks geinspecteerd?",
                    "answer_type": "List",
                    "required": False,
                    "order": 7,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Verlichting conventioneel of LED?",
                    "answer_type": "List",
                    "required": True,
                    "order": 8,
                    "options": [
                        {"value": "Conventioneel"},
                        {"value": "Mix conventioneel en LED"},
                        {"value": "LED"},
                    ],
                },
                {
                    "text": "Aantal conventionele armaturen?",
                    "answer_type": "Number",
                    "required": False,
                    "order": 9,
                    "unit": "st",
                },
                {
                    "text": "Staat van de conventionele armaturen?",
                    "answer_type": "List",
                    "required": False,
                    "order": 10,
                    "options": [
                        {"value": "Slecht"},
                        {"value": "Redelijk"},
                        {"value": "Normaal"},
                        {"value": "Goed"},
                    ],
                },
                {
                    "text": "Intercomsysteem aanwezig?",
                    "answer_type": "List",
                    "required": True,
                    "order": 11,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Status van het intercomsysteem?",
                    "answer_type": "List",
                    "required": False,
                    "order": 12,
                    "options": [
                        {"value": "Slecht"},
                        {"value": "Matig"},
                        {"value": "Redelijk"},
                        {"value": "Goed"},
                    ],
                },
                {
                    "text": "Foto van het intercom systeem (postkast)",
                    "answer_type": "External Document",
                    "required": False,
                    "order": 13,
                },
                {
                    "text": "Foto van het intercomsysteem (belletableau)",
                    "answer_type": "External Document",
                    "required": False,
                    "order": 14,
                },
                {
                    "text": "Bliksembeveiliging aanwezig?",
                    "answer_type": "List",
                    "required": True,
                    "order": 15,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                    ],
                },
                {
                    "text": "Verdeelinrichting(-en)",
                    "answer_type": "Header",
                    "required": False,
                    "order": 16,
                },
                {
                    "text": "Foto van de verdeelinrichting",
                    "answer_type": "External Document",
                    "required": True,
                    "order": 17,
                },
                {
                    "text": "Aardlekschakelaar aanwezig i.c.m. algemene wcd's?",
                    "answer_type": "List",
                    "required": True,
                    "order": 18,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                        {"value": "n.v.t."},
                    ],
                },
                {
                    "text": "Status verdeelinrichting(-en)",
                    "answer_type": "List",
                    "required": True,
                    "order": 19,
                    "options": [
                        {"value": "Slecht"},
                        {"value": "Matig"},
                        {"value": "Redelijk"},
                        {"value": "Goed"},
                    ],
                },
                {
                    "text": "Algemene aarding in orde?",
                    "answer_type": "List",
                    "required": True,
                    "order": 20,
                    "options": [
                        {"value": "Ja"},
                        {"value": "Nee"},
                        {"value": "n.v.t."},
                    ],
                },
                {
                    "text": "Naam servicemonteur",
                    "answer_type": "Text",
                    "required": True,
                    "order": 21,
                },
                {
                    "text": "Handtekening servicemonteur",
                    "answer_type": "Signature",
                    "required": True,
                    "order": 22,
                },
            ],
            "dependencies": [
                {
                    "parent_question_order": 1,
                    "trigger_value": "Ja",
                    "child_question_order": 2,
                },
                {
                    "parent_question_order": 1,
                    "trigger_value": "Nee",
                    "child_question_order": 3,
                },
                {
                    "parent_question_order": 4,
                    "trigger_value": "Ja",
                    "child_question_order": 5,
                },
                {
                    "parent_question_order": 6,
                    "trigger_value": "Ja",
                    "child_question_order": 7,
                },
                {
                    "parent_question_order": 8,
                    "trigger_value": "Conventioneel",
                    "child_question_order": 9,
                },
                {
                    "parent_question_order": 8,
                    "trigger_value": "Mix conventioneel en LED",
                    "child_question_order": 9,
                },
                {
                    "parent_question_order": 8,
                    "trigger_value": "Conventioneel",
                    "child_question_order": 10,
                },
                {
                    "parent_question_order": 8,
                    "trigger_value": "Mix conventioneel en LED",
                    "child_question_order": 10,
                },
                {
                    "parent_question_order": 11,
                    "trigger_value": "Ja",
                    "child_question_order": 12,
                },
                {
                    "parent_question_order": 12,
                    "trigger_value": "Slecht",
                    "child_question_order": 13,
                },
                {
                    "parent_question_order": 12,
                    "trigger_value": "Matig",
                    "child_question_order": 13,
                },
                {
                    "parent_question_order": 12,
                    "trigger_value": "Slecht",
                    "child_question_order": 14,
                },
                {
                    "parent_question_order": 12,
                    "trigger_value": "Matig",
                    "child_question_order": 14,
                },
            ],
        },
    ],
}


async def truncate_checklist_tables() -> None:
    conn = Tortoise.get_connection("default")
    # Order and names chosen to match Tortoise defaults in this project
    statements: List[str] = [
        "TRUNCATE TABLE checklistresponse RESTART IDENTITY CASCADE;",
        "TRUNCATE TABLE questiondependency RESTART IDENTITY CASCADE;",
        "TRUNCATE TABLE listoption RESTART IDENTITY CASCADE;",
        "TRUNCATE TABLE question RESTART IDENTITY CASCADE;",
        "TRUNCATE TABLE checklist RESTART IDENTITY CASCADE;",
        "TRUNCATE TABLE answertype RESTART IDENTITY CASCADE;",
        "TRUNCATE TABLE unit RESTART IDENTITY CASCADE;",
    ]
    for stmt in statements:
        await conn.execute_script(stmt)


async def populate_units(data: Dict[str, Any]) -> None:
    for unit_data in data.get("units", []):
        await Unit.create(**unit_data)


async def populate_answer_types(data: Dict[str, Any]) -> None:
    for at_data in data.get("answer_types", []):
        await AnswerType.create(**at_data)


async def populate_checklists(data: Dict[str, Any]) -> None:
    for cl_data in data.get("checklists", []):
        checklist = await Checklist.create(
            name=cl_data["name"], description=cl_data.get("description", "")
        )

        question_by_order: Dict[int, Question] = {}

        for q_data in cl_data.get("questions", []):
            options_data: List[Dict[str, str]] = q_data.pop("options", [])
            answer_type_name: str = q_data.pop("answer_type")
            unit_code: Optional[str] = q_data.pop("unit", None)
            recognition_model: Optional[str] = q_data.pop("recognition_model", None)

            try:
                answer_type = await AnswerType.get(name=answer_type_name)
            except Exception:
                # Skip invalid answer types
                continue

            unit: Optional[Unit] = None
            if unit_code:
                try:
                    unit = await Unit.get(code=unit_code)
                except Exception:
                    unit = None

            question = await Question.create(
                checklist=checklist,
                answer_type=answer_type,
                unit=unit,
                recognition_model=recognition_model,
                **q_data,
            )
            question_by_order[question.order] = question

            if answer_type.name == "List":
                for opt_data in options_data:
                    await ListOption.create(question=question, **opt_data)

        for dep in cl_data.get("dependencies", []):
            parent = question_by_order.get(dep["parent_question_order"])
            child = question_by_order.get(dep["child_question_order"])
            if not parent or not child:
                continue
            try:
                trigger_option = await ListOption.get(
                    question=parent, value=dep["trigger_value"]
                )
            except Exception:
                continue
            await QuestionDependency.create(
                parent_question=parent,
                child_question=child,
                trigger_option=trigger_option,
            )


async def main() -> None:
    print("Initializing Tortoise ORM...")
    await Tortoise.init(config=TORTOISE_ORM)
    # Ensure schemas exist (noop if already created via migrations)
    await Tortoise.generate_schemas(safe=True)

    print("Truncating existing checklist tables and resetting IDs...")
    await truncate_checklist_tables()
    print("All checklist tables truncated and IDs reset.")

    print("Populating Units...")
    await populate_units(DATA)
    units_count = await Unit.all().count()
    print(f"Populated {units_count} Units.")

    print("Populating AnswerTypes...")
    await populate_answer_types(DATA)
    at_count = await AnswerType.all().count()
    print(f"Populated {at_count} AnswerTypes.")

    print("Populating Checklists, Questions, Options, and Dependencies...")
    await populate_checklists(DATA)
    cl_count = await Checklist.all().count()
    q_count = await Question.all().count()
    opt_count = await ListOption.all().count()
    dep_count = await QuestionDependency.all().count()
    print(
        f"Populated {cl_count} Checklists, {q_count} Questions, {opt_count} ListOptions, {dep_count} QuestionDependencies."
    )

    await Tortoise.close_connections()
    print("Database population complete.")


if __name__ == "__main__":
    asyncio.run(main())
