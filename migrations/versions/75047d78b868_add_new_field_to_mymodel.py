from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '75047d78b868'
down_revision = 'f1f749a7d29e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Включаем "batch mode" для управления таблицей
    with op.batch_alter_table('users') as batch_op:
        # Проверяем, существует ли столбец (опционально, если вы это добавляли ранее)
        if not has_column('users', 'telegram_id'):
            batch_op.add_column(sa.Column('telegram_id', sa.Integer(), nullable=False, server_default='0'))
        # Убираем значение по умолчанию
        batch_op.alter_column('telegram_id', server_default=None)
        # Создаём уникальное ограничение
        batch_op.create_unique_constraint('uq_users_telegram_id', ['telegram_id'])


def downgrade() -> None:
    # Удаляем столбец и ограничения через "batch mode"
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_constraint('uq_users_telegram_id', type_='unique')
        batch_op.drop_column('telegram_id')


def has_column(table_name: str, column_name: str) -> bool:
    """
    Проверяет, существует ли столбец в таблице.
    """
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns
