from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from support_agent_rag import create_app
from support_agent_rag.db.models import Base
from support_agent_rag.db.repository import seed_database
from support_agent_rag.seed.generator import generate_dataset


def test_api_can_read_from_database_backed_shop() -> None:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_database(
            session,
            generate_dataset(seed=21, customers_count=2, products_count=2, orders_count=2),
        )
        session.commit()

    response = TestClient(create_app(database_engine=engine)).get(
        "/shop/orders/order-0001",
        headers={"Authorization": "Bearer operator-token"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == "order-0001"
