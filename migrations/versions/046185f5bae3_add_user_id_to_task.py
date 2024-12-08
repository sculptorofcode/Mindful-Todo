from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '046185f5bae3'
down_revision = 'f14b2b40afc1'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the 'user_id' column with nullable=True
    with op.batch_alter_table('tbl_tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=36), nullable=True))

    # Step 2: Update existing tasks with a default 'user_id' (can be a UUID or some other value)
    op.execute("UPDATE tbl_tasks SET user_id = 'default-user-id' WHERE user_id IS NULL")

    # Step 3: Alter the column to make it NOT NULL
    with op.batch_alter_table('tbl_tasks', schema=None) as batch_op:
        batch_op.alter_column('user_id', nullable=False)

def downgrade():
    with op.batch_alter_table('tbl_tasks', schema=None) as batch_op:
        batch_op.drop_column('user_id')
