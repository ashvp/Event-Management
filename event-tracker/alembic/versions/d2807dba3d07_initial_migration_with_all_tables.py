"""Initial migration with all tables

Revision ID: d2807dba3d07
Revises: 0e5788fa6e33
Create Date: 2025-05-16 19:35:03.375911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd2807dba3d07'
down_revision: Union[str, None] = '0e5788fa6e33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

roleenum = postgresql.ENUM('attendee', 'speaker', 'organizer', name='roleenum')
def upgrade() -> None:
    # Create enum type if not exists (avoids duplicate error)
    
    roleenum.create(op.get_bind(), checkfirst=True)

    op.create_table('attendees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('attendee', 'speaker', 'organizer', name='roleenum'), nullable=True),
        sa.Column('rfid_uid', sa.String(), nullable=True),
        sa.Column('registered', sa.Boolean(), nullable=True),
        sa.Column('got_kit', sa.Boolean(), nullable=True),
        sa.Column('got_lunch', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rfid_uid')
    )
    op.create_index(op.f('ix_attendees_email'), 'attendees', ['email'], unique=True)
    op.create_index(op.f('ix_attendees_id'), 'attendees', ['id'], unique=False)

    op.create_table('event_days',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_days_date'), 'event_days', ['date'], unique=True)
    op.create_index(op.f('ix_event_days_id'), 'event_days', ['id'], unique=False)

    op.create_table('attendances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('attendee_id', sa.Integer(), nullable=False),
        sa.Column('event_day_id', sa.Integer(), nullable=False),
        sa.Column('checked_in', sa.Boolean(), nullable=True),
        sa.Column('got_kit', sa.Boolean(), nullable=True),
        sa.Column('got_lunch', sa.Boolean(), nullable=True),
        sa.Column('got_freebies', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['attendee_id'], ['attendees.id']),
        sa.ForeignKeyConstraint(['event_day_id'], ['event_days.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendances_id'), 'attendances', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_attendances_id'), table_name='attendances')
    op.drop_table('attendances')
    op.drop_index(op.f('ix_event_days_id'), table_name='event_days')
    op.drop_index(op.f('ix_event_days_date'), table_name='event_days')
    op.drop_table('event_days')
    op.drop_index(op.f('ix_attendees_id'), table_name='attendees')
    op.drop_index(op.f('ix_attendees_email'), table_name='attendees')
    op.drop_table('attendees')
    # Drop enum type if exists
    roleenum.drop(op.get_bind(), checkfirst=True)