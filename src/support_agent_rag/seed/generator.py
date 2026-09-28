import random
from dataclasses import dataclass


@dataclass(frozen=True)
class SeedCustomer:
    id: str
    name: str
    email: str


@dataclass(frozen=True)
class SeedProduct:
    id: str
    name: str
    category: str
    price: float


@dataclass(frozen=True)
class SeedOrderItem:
    id: str
    product_id: str
    quantity: int
    price: float


@dataclass(frozen=True)
class SeedOrder:
    id: str
    customer_id: str
    status: str
    total: float
    items: tuple[SeedOrderItem, ...]


@dataclass(frozen=True)
class SeedDataset:
    customers: tuple[SeedCustomer, ...]
    products: tuple[SeedProduct, ...]
    orders: tuple[SeedOrder, ...]


def generate_dataset(
    seed: int = 42,
    customers_count: int = 50,
    products_count: int = 100,
    orders_count: int = 500,
) -> SeedDataset:
    """Generate reproducible synthetic shop data without real PII."""
    rng = random.Random(seed)
    customers = tuple(
        SeedCustomer(
            id=f"customer-{index:04d}",
            name=f"Customer {index:04d}",
            email=f"customer-{index:04d}@example.test",
        )
        for index in range(1, customers_count + 1)
    )
    products = tuple(
        SeedProduct(
            id=f"product-{index:04d}",
            name=f"TechShop Product {index:04d}",
            category=rng.choice(("audio", "cables", "mobile", "accessories")),
            price=round(rng.uniform(9.99, 499.99), 2),
        )
        for index in range(1, products_count + 1)
    )
    orders = []
    statuses = ("processing", "shipped", "delivered")
    for index in range(1, orders_count + 1):
        item_product = rng.choice(products)
        quantity = rng.randint(1, 3)
        item = SeedOrderItem(
            id=f"item-{index:04d}",
            product_id=item_product.id,
            quantity=quantity,
            price=item_product.price,
        )
        orders.append(
            SeedOrder(
                id=f"order-{index:04d}",
                customer_id=rng.choice(customers).id,
                status=rng.choice(statuses),
                total=round(item.price * quantity, 2),
                items=(item,),
            )
        )
    return SeedDataset(customers, products, tuple(orders))
