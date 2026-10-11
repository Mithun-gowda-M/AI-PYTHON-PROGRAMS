"""Match automobile symptoms to rule-based faults and suggested actions."""

RULES = {
    "Battery failure": ({"difficulty_starting", "dim_lights"}, "Check the battery and charging system; replace the battery if needed."),
    "Engine overheating": ({"high_temperature", "steam_from_engine"}, "Stop safely, let the engine cool, then check coolant and the radiator."),
    "Brake problem": ({"soft_brake", "squeaking_noise"}, "Have the brake pads and brake fluid inspected promptly."),
}


def diagnose(symptoms: set[str]) -> list[tuple[str, str]]:
    return [
        (fault, action)
        for fault, (required, action) in RULES.items()
        if required <= symptoms
    ]


def main() -> None:
    observed = {"difficulty_starting", "dim_lights"}
    print("Observed symptoms:", ", ".join(sorted(observed)))
    matches = diagnose(observed)
    if not matches:
        print("No rule matched the supplied symptoms.")
    for fault, action in matches:
        print("Possible fault:", fault)
        print("Suggested action:", action)
    print("This rule-based example is not a substitute for a qualified mechanic.")


if __name__ == "__main__":
    main()
