import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..db.models import Base
from ..db.repository import seed_database
from .generator import generate_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed synthetic TechShop data")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--customers", type=int, default=50)
    parser.add_argument("--products", type=int, default=100)
    parser.add_argument("--orders", type=int, default=500)
    args = parser.parse_args()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    dataset = generate_dataset(
        seed=args.seed,
        customers_count=args.customers,
        products_count=args.products,
        orders_count=args.orders,
    )
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_database(session, dataset)
        session.commit()
    print(
        f"Seeded customers={len(dataset.customers)} "
        f"products={len(dataset.products)} orders={len(dataset.orders)}"
    )


if __name__ == "__main__":
    main()
