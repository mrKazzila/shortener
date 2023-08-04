from sqlalchemy import Boolean, Column, Integer, String, Table, MetaData

metadata = MetaData()

url = Table(
    'url',
    metadata,
    Column(
        name='id',
        type_=Integer,
        primary_key=True,
    ),
    Column(
        name='key',
        type_=Integer,
        unique=True,
        index=True
    ),
    Column(
        name='secret_key',
        type_=String,
        unique=True,
        index=True,
    ),
    Column(
        name='target_url',
        type_=String,
        index=True,
    ),
    Column(
        name='is_active',
        type_=Boolean,
        default=True,
    ),
    Column(
        name='clicks_count',
        type_=Integer,
        default=0,
    ),
)
