"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2026-01-10 00:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create wines table
    op.create_table('wines',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('producer', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('region', sa.String(), nullable=False),
        sa.Column('volume_ml', sa.Integer(), nullable=False),
        sa.Column('vintage_year', sa.Integer(), nullable=False),
        sa.Column('glasses_per_bottle', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('RED', 'WHITE', 'ROSE', 'SPARKLING', 'DESSERT', 'FORTIFIED', name='winetype'), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(), nullable=True),
        sa.Column('grape_variety', sa.String(), nullable=True),
        sa.Column('alcohol_percentage', sa.Float(), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('sku', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_wines_id'), 'wines', ['id'], unique=False)

    # Create inventories table
    op.create_table('inventories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wine_id', sa.Integer(), nullable=False),
        sa.Column('location_type', sa.Enum('WAREHOUSE', 'BAR_RESTAURANT', name='locationtype'), nullable=False),
        sa.Column('bottles_count', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['wine_id'], ['wines.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventories_id'), 'inventories', ['id'], unique=False)

    # Create sales table
    op.create_table('sales',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wine_id', sa.Integer(), nullable=False),
        sa.Column('sale_type', sa.Enum('BOTTLE', 'GLASS', name='saletype'), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('location_type', sa.Enum('WAREHOUSE', 'BAR_RESTAURANT', name='locationtype'), nullable=False),
        sa.Column('sale_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['wine_id'], ['wines.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_id'), 'sales', ['id'], unique=False)

    # Create orders table
    op.create_table('orders',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('customer_name', sa.String(), nullable=True),
        sa.Column('customer_email', sa.String(), nullable=True),
        sa.Column('shipping_address', sa.Text(), nullable=True),
        sa.Column('postal_code', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('shipping_cost', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('payment_status', sa.String(), nullable=True),
        sa.Column('order_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('shipped_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)

    # Create order_items table
    op.create_table('order_items',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('wine_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['wine_id'], ['wines.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)

    # Create adjustments table
    op.create_table('adjustments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wine_id', sa.Integer(), nullable=False),
        sa.Column('location_type', sa.Enum('WAREHOUSE', 'BAR_RESTAURANT', name='locationtype'), nullable=False),
        sa.Column('adjustment_type', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('adjusted_by', sa.String(), nullable=True),
        sa.Column('adjustment_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['wine_id'], ['wines.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adjustments_id'), 'adjustments', ['id'], unique=False)

    # Create vivino_mappings table
    op.create_table('vivino_mappings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wine_id', sa.Integer(), nullable=False),
        sa.Column('vivino_id', sa.String(), nullable=False),
        sa.Column('vivino_url', sa.String(), nullable=True),
        sa.Column('last_synced', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['wine_id'], ['wines.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vivino_mappings_id'), 'vivino_mappings', ['id'], unique=False)

    # Create shopify_syncs table
    op.create_table('shopify_syncs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wine_id', sa.Integer(), nullable=False),
        sa.Column('shopify_product_id', sa.String(), nullable=False),
        sa.Column('shopify_variant_id', sa.String(), nullable=True),
        sa.Column('last_synced', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['wine_id'], ['wines.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shopify_syncs_id'), 'shopify_syncs', ['id'], unique=False)


def downgrade():
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_shopify_syncs_id'), table_name='shopify_syncs')
    op.drop_table('shopify_syncs')
    
    op.drop_index(op.f('ix_vivino_mappings_id'), table_name='vivino_mappings')
    op.drop_table('vivino_mappings')
    
    op.drop_index(op.f('ix_adjustments_id'), table_name='adjustments')
    op.drop_table('adjustments')
    
    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.drop_table('order_items')
    
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    
    op.drop_index(op.f('ix_sales_id'), table_name='sales')
    op.drop_table('sales')
    
    op.drop_index(op.f('ix_inventories_id'), table_name='inventories')
    op.drop_table('inventories')
    
    op.drop_index(op.f('ix_wines_id'), table_name='wines')
    op.drop_table('wines')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS winetype')
    op.execute('DROP TYPE IF EXISTS locationtype')
    op.execute('DROP TYPE IF EXISTS saletype')