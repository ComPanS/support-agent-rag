from fastapi.testclient import TestClient

from support_agent_rag import create_app
from support_agent_rag.mock_shop.service import InMemoryShop

CLIENT_TOKEN = "client-token-alice"
OPERATOR_TOKEN = "operator-token"


def make_client() -> TestClient:
    return TestClient(create_app(shop=InMemoryShop.seeded()))


def test_customer_can_read_owned_order() -> None:
    response = make_client().get(
        "/shop/orders/order-1001",
        headers={"Authorization": f"Bearer {CLIENT_TOKEN}"},
    )

    assert response.status_code == 200
    assert response.json()["customer_id"] == "customer-001"
    assert response.json()["status"] == "shipped"


def test_customer_cannot_read_another_customers_order() -> None:
    response = make_client().get(
        "/shop/orders/order-1002",
        headers={"Authorization": f"Bearer {CLIENT_TOKEN}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_missing_order_returns_controlled_not_found() -> None:
    response = make_client().get(
        "/shop/orders/does-not-exist",
        headers={"Authorization": f"Bearer {CLIENT_TOKEN}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_operator_can_create_return_request() -> None:
    response = make_client().post(
        "/shop/orders/order-1001/returns",
        headers={"Authorization": f"Bearer {OPERATOR_TOKEN}"},
        json={"item_id": "item-1001", "reason": "defect"},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_client_cannot_perform_write_operation() -> None:
    response = make_client().post(
        "/shop/orders/order-1001/returns",
        headers={"Authorization": f"Bearer {CLIENT_TOKEN}"},
        json={"item_id": "item-1001", "reason": "defect"},
    )

    assert response.status_code == 403
