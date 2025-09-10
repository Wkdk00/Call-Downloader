"""v1.1

Revision ID: ea07d9386a97
Revises: caf0835a94b8
Create Date: 2025-06-26 13:31:27.610922

"""
from typing import Sequence, Union
from passlib.context import CryptContext
from sqlalchemy.sql import table, column
from dotenv import load_dotenv
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea07d9386a97'
down_revision: Union[str, None] = 'caf0835a94b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def upgrade() -> None:
    load_dotenv()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    users_table = table(
        'users',
        column('username', sa.String),
        column('hashed_password', sa.String),
    )

    op.execute(users_table.delete())

    hashed_password = bcrypt_context.hash(password)

    op.bulk_insert(
        users_table,
        [
            {"username": username, "hashed_password": hashed_password}
        ]
    )

def downgrade() -> None:
    op.execute("DELETE FROM users WHERE username = 'autoopt-call-robot'")
