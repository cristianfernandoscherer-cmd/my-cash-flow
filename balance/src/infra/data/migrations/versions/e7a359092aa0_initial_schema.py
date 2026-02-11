"""initial_schema

Revision ID: e7a359092aa0
Revises: 
Create Date: 2026-02-09 23:37:18.500380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7a359092aa0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create Transactions Table with complete schema
    op.execute("""
        CREATE TABLE transactions (
            id SERIAL PRIMARY KEY,
            item VARCHAR(255) NOT NULL,
            valor DECIMAL(10,2) NOT NULL,
            data DATE NOT NULL,
            categoria VARCHAR(100) NOT NULL,
            transaction_type VARCHAR(50) NOT NULL DEFAULT 'expense',
            descricao TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Indices
    op.execute("CREATE INDEX idx_transactions_data ON transactions(data);")
    op.execute("CREATE INDEX idx_transactions_categoria ON transactions(categoria);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS transactions;")