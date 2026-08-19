from eduharness.simulator.persona import generate_student_response, load_persona


def test_load_persona_and_generate_response() -> None:
    persona = load_persona("configs/personas/weak_slow.yaml")
    out = generate_student_response(persona, "loops")
    assert persona.persona_id == "weak_slow"
    assert "loops" in out
