from eduharness.core.config import ConfigLoader


def test_load_default_contract() -> None:
    loader = ConfigLoader(base_dir=".")
    data = loader.load_yaml("configs/contracts/default_contract.yaml")
    assert data["contract_id"] == "python_intro_v1"
