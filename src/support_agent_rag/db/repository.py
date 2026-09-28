from sqlalchemy import select
from sqlalchemy.orm import Session

from ..seed.generator import SeedDataset
from .models import Customer, Order, OrderItem, Product


def seed_database(session: Session, dataset: SeedDataset) -> None:
    """Insert a dataset once, keeping repeated seed runs idempotent."""
    for customer in dataset.customers:
        if session.get(Customer, customer.id) is None:
            session.add(Customer(id=customer.id, name=customer.name, email=customer.email))
    for product in dataset.products:
        if session.get(Product, product.id) is None:
            session.add(
                Product(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    price=product.price,
                )
            )
    session.flush()
    for order in dataset.orders:
        if session.get(Order, order.id) is not None:
            continue
        session.add(
            Order(
                id=order.id,
                customer_id=order.customer_id,
                status=order.status,
                total=order.total,
                items=[
                    OrderItem(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                    )
                    for item in order.items
                ],
            )
        )


def get_order_for_customer(session: Session, order_id: str, customer_id: str) -> Order | None:
    """Return only an order owned by the requested customer."""
    return session.scalar(
        select(Order).where(Order.id == order_id, Order.customer_id == customer_id)
    )
