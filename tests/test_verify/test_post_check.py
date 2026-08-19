from eduharness.verify.post_check import post_check_output


def test_post_check_blocks_withhold_leak() -> None:
    result = post_check_output("withhold", "Here is the full code: def solve(): pass")
    assert result == "block"
