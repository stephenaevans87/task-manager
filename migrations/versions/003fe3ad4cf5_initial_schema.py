from alembic import op
import sqlalchemy as sa


revision = "initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True)
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("text", sa.String(255), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.String(50), nullable=False),
        sa.Column("completed_at", sa.String(50), nullable=True),
        sa.Column("priority", sa.String(50), nullable=False, server_default="medium"),
        sa.Column("category", sa.String(50), nullable=False, server_default="general"),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_tasks_user_id"
        )
    )


def downgrade():

    op.drop_table("tasks")
    op.drop_table("users")