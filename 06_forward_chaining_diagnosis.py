"""Infer possible diagnoses from symptoms using forward chaining."""

RULES = [
    (frozenset({"fever", "cough", "sore_throat"}), "Flu"),
    (frozenset({"fever", "headache", "body_pain", "rash"}), "Dengue"),
    (frozenset({"fever", "chills", "sweating"}), "Malaria"),
]


def forward_chaining(symptoms: set[str]) -> list[str]:
    """Apply rules repeatedly until no new facts are inferred."""
    facts = set(symptoms)
    diagnoses: list[str] = []
    changed = True
    while changed:
        changed = False
        for required, diagnosis in RULES:
            if required <= facts and diagnosis not in facts:
                facts.add(diagnosis)
                diagnoses.append(diagnosis)
                changed = True
    return diagnoses


def main() -> None:
    patient_symptoms = {"fever", "headache", "body_pain", "rash"}
    print("Observed symptoms:", ", ".join(sorted(patient_symptoms)))
    possible = forward_chaining(patient_symptoms)
    print("Possible rule matches:", ", ".join(possible) if possible else "None")
    print("Educational example only; it is not a medical diagnosis.")


if __name__ == "__main__":
    main()
