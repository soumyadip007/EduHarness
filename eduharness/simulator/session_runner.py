from __future__ import annotations

from dataclasses import dataclass

from eduharness.simulator.adversarial_injector import maybe_inject_adversarial


@dataclass
class SimSessionResult:
    turns: int
    adversarial_turns: int


def run_simulated_session(turns: int = 10, adversarial_ratio: float = 0.2) -> SimSessionResult:
    adv = 0
    for t in range(1, turns + 1):
        if maybe_inject_adversarial(t, adversarial_ratio):
            adv += 1
    return SimSessionResult(turns=turns, adversarial_turns=adv)
