from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from .mock_shop.service import InMemoryShop

TOKENS = {
    "client-token-alice": {"role": "client", "customer_id": "customer-001"},
    "operator-token": {"role": "operator", "customer_id": None},
}


class ReturnRequestInput(BaseModel):
    item_id: str
    reason: str


def health() -> dict[str, str]:
    return {"service": "support-agent-rag", "status": "ok"}


def create_app(shop: InMemoryShop | None = None) -> FastAPI:
    """Build the service with an injectable shop dependency."""
    shop = shop or InMemoryShop.seeded()
    app = FastAPI(title="Support Agent RAG")

    @app.get("/health")
    def health_endpoint() -> dict[str, str]:
        return health()

    def current_user(authorization: str | None) -> dict[str, str | None]:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required")
        user = TOKENS.get(authorization.removeprefix("Bearer "))
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user

    @app.get("/shop/orders/{order_id}")
    def get_order(order_id: str, authorization: str | None = Header(default=None)):
        user = current_user(authorization)
        customer_id = user["customer_id"] if user["role"] == "client" else None
        order = shop.get_order(order_id, customer_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @app.post("/shop/orders/{order_id}/returns", status_code=201)
    def create_return(
        order_id: str,
        payload: ReturnRequestInput,
        authorization: str | None = Header(default=None),
    ):
        user = current_user(authorization)
        if user["role"] != "operator":
            raise HTTPException(status_code=403, detail="Operator role required")
        request = shop.create_return_request(order_id, payload.item_id, payload.reason)
        if request is None:
            raise HTTPException(status_code=404, detail="Order or item not found")
        return request

    return app


app = create_app()
