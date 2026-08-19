from dataclasses import dataclass


@dataclass
class HarnessConfig:
    mode: str  # H0, H1, H2, H3, H0+M, H0+G
    enable_verify: bool = False
    enable_memory: bool = False
    enable_govern: bool = False


def get_harness_config(mode: str) -> HarnessConfig:
    mapping = {
        "H0": HarnessConfig(mode="H0"),
        "H1": HarnessConfig(mode="H1", enable_verify=True),
        "H2": HarnessConfig(mode="H2", enable_verify=True, enable_memory=True),
        "H3": HarnessConfig(mode="H3", enable_verify=True, enable_memory=True, enable_govern=True),
        "H0+M": HarnessConfig(mode="H0+M", enable_memory=True),
        "H0+G": HarnessConfig(mode="H0+G", enable_govern=True),
    }
    return mapping.get(mode, mapping["H0"])
