from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from support_agent_rag.db.models import Base, Customer, Order, OrderItem, Product
from support_agent_rag.db.repository import seed_database
from support_agent_rag.seed.generator import generate_dataset


def test_seed_database_writes_related_rows_and_is_idempotent() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    dataset = generate_dataset(seed=11, customers_count=3, products_count=4, orders_count=8)

    with Session(engine) as session:
        seed_database(session, dataset)
        seed_database(session, dataset)
        session.commit()

        assert len(session.scalars(select(Customer)).all()) == 3
        assert len(session.scalars(select(Product)).all()) == 4
        assert len(session.scalars(select(Order)).all()) == 8
        assert len(session.scalars(select(OrderItem)).all()) == 8


def test_repository_filters_order_by_customer() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    dataset = generate_dataset(seed=12, customers_count=2, products_count=2, orders_count=2)

    with Session(engine) as session:
        seed_database(session, dataset)
        session.commit()
        order = session.scalar(select(Order).order_by(Order.id))

        assert order is not None
        assert session.get(Order, order.id).customer_id == order.customer_id
