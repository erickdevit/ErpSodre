"""receitas oftalmologicas completas com validade e perto"""

from alembic import op
import sqlalchemy as sa


# ESSAS DUAS LINHAS O ALEMBIC JÁ GEROU PRA VOCÊ — NÃO MUDE NADA!
revision = 'a1b2c3d4e5f6'          # ← o ID que apareceu no seu arquivo
down_revision = 'ca4d36a65e4e'     # ← o ID da migração anterior (a última que deu certo)
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('receitas_oftalmologicas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True),
        
        sa.Column('data_emissao', sa.Date(), nullable=False),
        sa.Column('validade_em', sa.Date(), nullable=False),           # novo
        sa.Column('medico', sa.String(), nullable=True),
        sa.Column('crm', sa.String(), nullable=True),

        # Longe
        sa.Column('od_esf_long', sa.String(), nullable=False),
        sa.Column('od_cil_long', sa.String(), nullable=True),
        sa.Column('od_eixo_long', sa.String(), nullable=True),
        sa.Column('oe_esf_long', sa.String(), nullable=False),
        sa.Column('oe_cil_long', sa.String(), nullable=True),
        sa.Column('oe_eixo_long', sa.String(), nullable=True),

        # Perto (calculado)
        sa.Column('od_esf_perto', sa.String(), nullable=True),
        sa.Column('oe_esf_perto', sa.String(), nullable=True),

        # Adição e medidas
        sa.Column('adicao', sa.String(), nullable=True),
        sa.Column('dnp_od', sa.String(), nullable=True),
        sa.Column('dnp_oe', sa.String(), nullable=True),
        sa.Column('altura_od', sa.String(), nullable=True),
        sa.Column('altura_oe', sa.String(), nullable=True),

        sa.Column('observacoes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),

        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_receitas_cliente_id', 'receitas_oftalmologicas', ['cliente_id'])


def downgrade():
    op.drop_index('ix_receitas_cliente_id', table_name='receitas_oftalmologicas')
    op.drop_table('receitas_oftalmologicas')