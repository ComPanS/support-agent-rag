from support_agent_rag.seed.generator import generate_dataset


def test_seed_generator_is_deterministic_and_has_expected_shape() -> None:
    first = generate_dataset(seed=7, customers_count=3, products_count=4, orders_count=8)
    second = generate_dataset(seed=7, customers_count=3, products_count=4, orders_count=8)

    assert first == second
    assert len(first.customers) == 3
    assert len(first.products) == 4
    assert len(first.orders) == 8
    assert all(order.items for order in first.orders)
