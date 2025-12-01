"""clientes: endereco detalhado — versão FINAL 100% compatível com SQLite"""

from alembic import op
import sqlalchemy as sa

revision = 'ca4d36a65e4e'
down_revision = '0e7c15034e57'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Criar tabela temporária com a estrutura FINAL (com UNIQUE já dentro)
    op.create_table('clientes_temp',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(), nullable=False, index=True),
        sa.Column('telefone', sa.String(), nullable=True),
        
        # Endereço detalhado
        sa.Column('cep', sa.String(), nullable=True),
        sa.Column('logradouro', sa.String(), nullable=True),
        sa.Column('numero', sa.String(), nullable=True),
        sa.Column('complemento', sa.String(), nullable=True),
        sa.Column('bairro', sa.String(), nullable=True),
        sa.Column('cidade', sa.String(), nullable=True),
        sa.Column('estado', sa.String(), nullable=True),
        
        # Dados pessoais
        sa.Column('cpf', sa.String(), nullable=True, unique=True, index=True),
        sa.Column('rg', sa.String(), nullable=True, unique=True, index=True),
        sa.Column('data_nascimento', sa.Date(), nullable=True),
        sa.Column('sexo', sa.String(), nullable=True),
        sa.Column('pai', sa.String(), nullable=True),
        sa.Column('mae', sa.String(), nullable=True),
        sa.Column('observacoes', sa.String(), nullable=True),
        sa.Column('responsavel_id', sa.Integer(), sa.ForeignKey('clientes_temp.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # 2. Copiar todos os dados da tabela antiga
    op.execute("""
        INSERT INTO clientes_temp (
            id, nome, telefone, cpf, rg, data_nascimento, sexo, pai, mae,
            observacoes, responsavel_id, created_at
        )
        SELECT 
            id, nome, telefone, cpf, rg, data_nascimento, sexo, pai, mae,
            observacoes, responsavel_id, created_at
        FROM clientes
    """)

    # 3. Apagar tabela antiga e renomear
    op.drop_table('clientes')
    op.rename_table('clientes_temp', 'clientes')

    # 4. Recriar índice de nome (o único que não é unique)
    op.create_index('ix_clientes_nome', 'clientes', ['nome'])


def downgrade():
    # Não vamos usar mesmo, mas tem que ter
    pass