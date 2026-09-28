from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    status: Literal["processing", "shipped", "delivered"]
    total: float
    items: tuple[dict[str, str], ...]


@dataclass
class ReturnRequest:
    id: str
    order_id: str
    item_id: str
    reason: str
    status: Literal["pending"] = "pending"


@dataclass
class InMemoryShop:
    orders: dict[str, Order]
    return_requests: list[ReturnRequest] = field(default_factory=list)

    @classmethod
    def seeded(cls) -> "InMemoryShop":
        return cls(
            orders={
                "order-1001": Order(
                    id="order-1001",
                    customer_id="customer-001",
                    status="shipped",
                    total=129.99,
                    items=({"id": "item-1001", "name": "Wireless headphones"},),
                ),
                "order-1002": Order(
                    id="order-1002",
                    customer_id="customer-002",
                    status="delivered",
                    total=49.99,
                    items=({"id": "item-1002", "name": "USB-C cable"},),
                ),
            }
        )

    def get_order(self, order_id: str, customer_id: str | None = None) -> Order | None:
        order = self.orders.get(order_id)
        if order is None or (customer_id is not None and order.customer_id != customer_id):
            return None
        return order

    def create_return_request(
        self, order_id: str, item_id: str, reason: str
    ) -> ReturnRequest | None:
        order = self.orders.get(order_id)
        if order is None or not any(item["id"] == item_id for item in order.items):
            return None
        request = ReturnRequest(
            id=f"return-{len(self.return_requests) + 1:04d}",
            order_id=order_id,
            item_id=item_id,
            reason=reason,
        )
        self.return_requests.append(request)
        return request
