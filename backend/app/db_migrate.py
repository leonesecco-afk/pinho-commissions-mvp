from sqlalchemy import text
from .db import engine
import os


def run_migrations():
    """Run SQL statements from the migrations.sql file against the database."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_file = os.path.join(base_dir, 'sql', 'migrations.sql')
    # Read the SQL file contents
    with open(sql_file, 'r') as f:
        sql_content = f.read()
    # Split statements by semicolon and filter out empty statements
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    # Execute each statement within a transaction
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
    print("Migrations applied successfully.")


if __name__ == "__main__":
    run_migrations()
