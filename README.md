
# hinfelaar_fastapi

## Overview

Async FastAPI service with Tortoise ORM and Aerich migrations. Includes example `User` model and Django-like migration workflow.

## Requirements

- Python 3.10+
- PostgreSQL running locally on `localhost:5432` with a database named `hinfelaar_fastapi`
- The app currently uses a hardcoded DB URL. We'll move to `.env` soon.

Database URL:

```
postgres://hinfelaar_fastapi_db_user:hinfelaar_fastapi_db_password@localhost:5432/hinfelaar_fastapi
```

This URL is configured in `app/models/__init__.py` via `TORTOISE_ORM`.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```bash
# Option A: using the provided runner
python main.py

# Option B: direct uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open interactive docs: `http://localhost:8000/docs`

## PostgreSQL roles and permissions

When working locally you may want a single app user that can run migrations and manage objects. In production, avoid superuser and prefer a least‑privilege split between a migrator role and a runtime role.

### Fixing “permission denied to create database” locally

If your regular app user (`hinfelaar_fastapi_db_user`) cannot create/drop databases, use your admin user (e.g., `chriszuidema`) to recreate the DB and grant permissions:

```sql
-- Connect as admin
-- psql -U chriszuidema -d postgres

DROP DATABASE IF EXISTS hinfelaar_fastapi;
CREATE DATABASE hinfelaar_fastapi OWNER hinfelaar_fastapi_db_user;

-- Optional: allow the app user to create/drop databases locally
ALTER ROLE hinfelaar_fastapi_db_user CREATEDB;
-- Optional: if migrations create roles (usually not needed locally)
ALTER ROLE hinfelaar_fastapi_db_user CREATEROLE;

-- Inside the target database
-- \c hinfelaar_fastapi
GRANT ALL PRIVILEGES ON DATABASE hinfelaar_fastapi TO hinfelaar_fastapi_db_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO hinfelaar_fastapi_db_user;
ALTER SCHEMA public OWNER TO hinfelaar_fastapi_db_user;

-- Ensure future objects are accessible
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO hinfelaar_fastapi_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO hinfelaar_fastapi_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON FUNCTIONS TO hinfelaar_fastapi_db_user;
```

Then connect as the app user:

```bash
psql -U hinfelaar_fastapi_db_user -d hinfelaar_fastapi
```

### Production best practice (least privilege)

Use two roles: a migration role (CI/CD) that owns the application database/schema, and a runtime role for the app process.

```sql
-- Run as an admin/owner once
CREATE ROLE app_runtime LOGIN PASSWORD 'replace-me';
CREATE ROLE app_migrator LOGIN PASSWORD 'replace-me-too';

-- Make the migrator the owner of the application database
ALTER DATABASE hinfelaar_fastapi OWNER TO app_migrator;

-- Use a dedicated schema instead of public
CREATE SCHEMA IF NOT EXISTS app AUTHORIZATION app_migrator;

-- Minimal runtime rights
GRANT CONNECT ON DATABASE hinfelaar_fastapi TO app_runtime;
GRANT USAGE ON SCHEMA app TO app_runtime;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_runtime;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA app TO app_runtime;
ALTER ROLE app_runtime SET search_path = app, public;
-- Optional: allow creating tables at runtime (many apps do not need this)
GRANT CREATE ON SCHEMA app TO app_runtime;

-- Default privileges so future objects from migrations remain accessible
ALTER DEFAULT PRIVILEGES FOR ROLE app_migrator IN SCHEMA app
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE app_migrator IN SCHEMA app
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO app_runtime;
```

Notes:

- Do not grant SUPERUSER to application roles in production.
- In production you typically do not allow CREATEDB on the migrator; database provisioning is handled separately.
- Many managed services restrict superuser; prefer the grants above.

## Schema management modes

We support two modes:

- Prototype-fast (default now): The app sets `generate_schemas=True` on startup, so tables are auto-created when the DB is empty. An idempotent startup SQL ensures the JSONB GIN index exists. This makes it easy to drop/recreate the DB without touching migrations.
- Production-disciplined: Disable auto-generate, manage changes via Aerich migrations only.

To switch modes: in `app/main.py` change `generate_schemas` accordingly.

## Tortoise ORM + Aerich (migrations)

This setup mirrors Django's makemigrations/migrate flow.

1) Initialize Aerich (one-time):

```bash
aerich init -t app.models.TORTOISE_ORM
```

2) Create the database schema from current models (one-time for a new project):

```bash
aerich init-db
```

3) Make migrations when models change:

```bash
aerich migrate --name update_models
```

4) Apply migrations:

```bash
aerich upgrade
```

Notes:

- Ensure your PostgreSQL user/database matches the hardcoded credentials in `app/models/__init__.py` for now.
- The `aerich init` command will create an `aerich.ini` and a `migrations` directory.
- In prototype mode, `generate_schemas` is enabled. When your schema stabilizes, run `aerich init-db` to create a baseline and then set `generate_schemas=False` to move to migrations-only.
- If you add new model modules, include them in `TORTOISE_ORM["apps"]["models"]["models"]` in `app/models/__init__.py` (e.g., `"app.models.checklist"`, `"app.models.rating"`).

### Django → Tortoise migration tips

- Field differences:
  - JSONField: Use PostgreSQL JSONB with a GIN index for performance. We add the index via a migration and a startup safety check.
  - `unique_together` must be a tuple of tuples, e.g. `(("checklist", "order"),)`.
  - Use Tortoise `on_delete` constants: `fields.CASCADE`, `fields.SET_NULL`, `fields.RESTRICT`.
- Migration order can be wrong when many models are added:
  - If `aerich upgrade` fails with “relation does not exist”, open the generated migration and reorder `CREATE TABLE` statements so referenced tables exist first.
  - Recommended order for checklist models: `unit`, `answertype`, `checklist`, `question`, `listoption`, `questiondependency`, `checklistresponse`.
- Safer workflows:
  - Add models in smaller batches: migrate base tables first, then dependents.
  - Or create an empty migration and paste SQL in the correct order:
    - `aerich migrate --empty --name manual_order`
  - For initial bootstraps, you can generate schemas once and then snapshot baseline:
    - Programmatically call `Tortoise.init(...)` then `await Tortoise.generate_schemas()`
    - Then run `aerich init-db` to create the baseline migration state
- Non-interactive usage (CI):
  - `aerich migrate --name change --no-input`
  - Keep the `models` list in `TORTOISE_ORM` stable and explicit to avoid flaky diffs

## Project Structure

```
app/
  main.py                      # FastAPI app with Tortoise registered
  models/
    __init__.py                # Tortoise config (TORTOISE_ORM)
    user.py                    # Example User model
    rating.py                  # Work order rating model (table: workorder_rating)
    checklist.py               # Checklist domain models (Unit, AnswerType, Checklist, Question, ListOption, QuestionDependency, ChecklistResponse)
  routers/
  schemas/
  services/
main.py                        # Entrypoint that runs uvicorn
```

## Example Model

See `app/models/user.py` for a simple `User` model. After running `aerich init-db` you can interact with it via Tortoise in your services/routers.

## Next Steps

- Switch DB config to environment variables (.env) using `python-dotenv` or similar.
- Add more models and migrations as needed.

## JSONB indexing for checklist responses

We store checklist answers in a JSONB column (`checklistresponse.answers`). To speed up queries that filter into this JSON (e.g., `answers->'foo' ? 'bar'`, containment `@>`, etc.), we create a GIN index.

- Index creation (migration — optional):

  - We rely on a startup safety check (below) to ensure the index exists. If you prefer to manage this via migrations, create an empty migration and add the SQL:

    ```bash
    aerich migrate --empty --name add_answers_gin_index
    # then edit the generated file and add:
    ```

    ```sql
    CREATE INDEX IF NOT EXISTS idx_checklistresponse_answers_gin
    ON checklistresponse USING GIN (answers);
    ```

    Then apply it via:
    ```bash
    aerich upgrade
    ```
- Index creation (startup safety):

  - On app startup, we also execute an idempotent statement to ensure the index exists:
    ```sql
    CREATE INDEX IF NOT EXISTS idx_checklistresponse_answers_gin
    ON checklistresponse USING GIN (answers);
    ```
  - This runs quickly if the index already exists and ensures new environments are safe even before migrations run.
- How updates are handled:

  - PostgreSQL automatically maintains the index on INSERT/UPDATE/DELETE. No app code is needed to keep it in sync.
- Changing the index definition later:

  - The startup `IF NOT EXISTS` command will not update an existing index definition. To change operator classes (e.g., `jsonb_path_ops`) or other options, create a new migration that drops and recreates the index with the desired definition, for example:
    ```sql
    DROP INDEX IF EXISTS idx_checklistresponse_answers_gin;
    CREATE INDEX idx_checklistresponse_answers_gin
    ON checklistresponse USING GIN (answers jsonb_path_ops);
    ```
  - Run `aerich migrate --empty --name tweak_answers_index` and place the SQL there, then `aerich upgrade`.

### Example JSONB queries that use the GIN index

Depending on the operator class, PostgreSQL will use the GIN index for:

- Containment queries:

  ```sql
  SELECT id FROM checklistresponse WHERE answers @> '{"key": "value"}';
  ```
- Existence/has key queries:

  ```sql
  SELECT id FROM checklistresponse WHERE answers ? 'key';
  ```

  Or any key from an array:

  ```sql
  SELECT id FROM checklistresponse WHERE answers ?| array['k1','k2'];
  ```

Note: Choose `jsonb_path_ops` if your workload is primarily containment (`@>`). The default GIN class supports a wider set of operators but may be larger/slower for containment-only workloads.
