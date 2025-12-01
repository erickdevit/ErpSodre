"""criar os completa com itens e funcionario"""

from alembic import op
import sqlalchemy as sa

revision = 'SEU_ID'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('funcionarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('cargo', sa.String(), nullable=True),
        sa.Column('telefone', sa.String(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('ordens_servico',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_os', sa.String(), nullable=False, unique=True),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('clientes.id'), nullable=False),
        sa.Column('receita_id', sa.Integer(), sa.ForeignKey('receitas_oftalmologicas.id'), nullable=True),
        sa.Column('funcionario_id', sa.Integer(), sa.ForeignKey('funcionarios.id'), nullable=True),
        sa.Column('data_registro', sa.DateTime(), nullable=False),
        sa.Column('tipo_lente', sa.Enum('surfaçada', 'pronta', name='tipolente'), nullable=False),
        sa.Column('valor_total', sa.Numeric(10,2), nullable=False),
        sa.Column('status', sa.Enum('Orçamento', 'Em produção', 'Pronto', 'Entregue', 'Cancelado', name='statusos'), nullable=False),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero_os')
    )

    op.create_table('itens_os',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ordem_id', sa.Integer(), sa.ForeignKey('ordens_servico.id', ondelete='CASCADE'), nullable=False),
        sa.Column('produto_id', sa.Integer(), sa.ForeignKey('produtos.id'), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('preco_unitario', sa.Numeric(10,2), nullable=False),
        sa.Column('subtotal', sa.Numeric(10,2), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('itens_os')
    op.drop_table('ordens_servico')
    op.drop_table('funcionarios')