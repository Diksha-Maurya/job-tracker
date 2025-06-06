"""create job_applications table

Revision ID: ce842d11ea5a
Revises: 
Create Date: 2025-04-10 01:22:57.160926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce842d11ea5a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_applications',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('position_title', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('applied', 'interview', 'rejected', 'offer', 'accepted', name='statusenum'), nullable=False),
    sa.Column('applied_on', sa.Date(), nullable=False),
    sa.Column('source', sa.String(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job_applications')
    # ### end Alembic commands ###
