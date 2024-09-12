"""init

Revision ID: 16a4d487429d
Revises: 
Create Date: 2024-09-12 17:17:47.631107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a4d487429d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customuser',
    sa.Column('email', sa.String(length=324), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('role', sa.Enum('user', 'manager', 'admin', 'owner', name='userrole'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email', name='uq_email')
    )
    op.create_table('track',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=10000), nullable=False),
    sa.Column('datetime_start', sa.DATE(), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=False),
    sa.Column('latitude_start', sa.FLOAT(), nullable=True),
    sa.Column('longitude_start', sa.FLOAT(), nullable=True),
    sa.Column('actual_route_length', sa.FLOAT(), nullable=True),
    sa.Column('gps_file', sa.JSON(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.CheckConstraint('LENGTH(author) >= 7 AND LENGTH(author) <= 255', name='check_author_length'),
    sa.CheckConstraint('LENGTH(description) >= 30 AND LENGTH(description) <= 10000', name='check_description_length'),
    sa.CheckConstraint('LENGTH(name) >= 7 AND LENGTH(name) <= 255', name='check_name_length'),
    sa.CheckConstraint('actual_route_length > 0 AND actual_route_length <= 200000', name='check_actual_route_length_range'),
    sa.CheckConstraint('latitude_start >= -90 AND latitude_start <= 90', name='check_latitude_start_range'),
    sa.CheckConstraint('longitude_start >= -180 AND longitude_start <= 180', name='check_longitude_start_range'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'author', 'datetime_start', name='uq_track')
    )
    op.create_table('uprofile',
    sa.Column('first_name', sa.String(length=124), nullable=False),
    sa.Column('last_name', sa.String(length=124), nullable=False),
    sa.Column('age', sa.SmallInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['customuser.id'], name='customuser.id'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('uprofile')
    op.drop_table('track')
    op.drop_table('customuser')
    # ### end Alembic commands ###