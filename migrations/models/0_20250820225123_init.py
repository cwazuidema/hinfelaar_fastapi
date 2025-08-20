from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "full_name" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "answertype" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE
);
COMMENT ON TABLE "answertype" IS 'Defines the type of an answer, e.g., Text, List, Value.';
CREATE TABLE IF NOT EXISTS "checklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT
);
COMMENT ON TABLE "checklist" IS 'Represents a checklist containing a set of questions.';
CREATE TABLE IF NOT EXISTS "checklistresponse" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "workordernumber" VARCHAR(50) NOT NULL,
    "bag" VARCHAR(50) NOT NULL,
    "answers" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "checklist_id" INT NOT NULL REFERENCES "checklist" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_checklistre_checkli_a7d9b6" UNIQUE ("checklist_id", "workordernumber", "bag", "answers")
);
COMMENT ON TABLE "checklistresponse" IS 'Represents a complete response to a checklist, including all answers and metadata.';
CREATE TABLE IF NOT EXISTS "unit" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(20) NOT NULL UNIQUE,
    "description" VARCHAR(255) NOT NULL
);
COMMENT ON TABLE "unit" IS 'Represents a unit of measurement, e.g., Amperes, Volts.';
CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" VARCHAR(255) NOT NULL,
    "required" BOOL NOT NULL DEFAULT False,
    "recognition_model" VARCHAR(50),
    "order" INT NOT NULL DEFAULT 0,
    "answer_type_id" INT NOT NULL REFERENCES "answertype" ("id") ON DELETE RESTRICT,
    "checklist_id" INT NOT NULL REFERENCES "checklist" ("id") ON DELETE CASCADE,
    "unit_id" INT REFERENCES "unit" ("id") ON DELETE SET NULL,
    CONSTRAINT "uid_question_checkli_3f356a" UNIQUE ("checklist_id", "order")
);
COMMENT ON TABLE "question" IS 'Represents a question in a checklist.';
CREATE TABLE IF NOT EXISTS "listoption" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "value" VARCHAR(100) NOT NULL,
    "question_id" INT NOT NULL REFERENCES "question" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "listoption" IS 'Provides a selectable option for questions of type ''List''.';
CREATE TABLE IF NOT EXISTS "questiondependency" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "child_question_id" INT NOT NULL REFERENCES "question" ("id") ON DELETE CASCADE,
    "parent_question_id" INT NOT NULL REFERENCES "question" ("id") ON DELETE CASCADE,
    "trigger_option_id" INT NOT NULL REFERENCES "listoption" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_questiondep_parent__c2abb4" UNIQUE ("parent_question_id", "trigger_option_id", "child_question_id")
);
COMMENT ON TABLE "questiondependency" IS 'Defines a dependency between two questions, where answering a parent';
CREATE TABLE IF NOT EXISTS "workorder_rating" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "werkboncode" VARCHAR(100) NOT NULL,
    "sessieid" INT NOT NULL,
    "value" INT NOT NULL,
    "omschrijving" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "uid_workorder_r_werkbon_21a663" UNIQUE ("werkboncode", "sessieid")
);
COMMENT ON COLUMN "workorder_rating"."werkboncode" IS 'Work order code';
COMMENT ON COLUMN "workorder_rating"."sessieid" IS 'Session ID for the work order';
COMMENT ON COLUMN "workorder_rating"."value" IS 'Rating value (e.g., 1-5 scale)';
COMMENT ON COLUMN "workorder_rating"."omschrijving" IS 'Optional description/comment for the rating';
COMMENT ON TABLE "workorder_rating" IS 'Model to store work order session ratings.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
