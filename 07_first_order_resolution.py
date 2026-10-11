"""A small first-order resolution prover for ground facts and unary rules.

Variables are terms beginning with '?'. This intentionally small example
supports predicate literals with atomic terms, unification, and binary
resolution; it is not a complete production theorem prover.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Literal:
    predicate: str
    args: tuple[str, ...]
    positive: bool = True


Clause = frozenset[Literal]


def dereference(term: str, substitution: dict[str, str]) -> str:
    while term.startswith("?") and term in substitution:
        term = substitution[term]
    return term


def unify(left: tuple[str, ...], right: tuple[str, ...]) -> dict[str, str] | None:
    if len(left) != len(right):
        return None
    substitution: dict[str, str] = {}
    for a, b in zip(left, right):
        a, b = dereference(a, substitution), dereference(b, substitution)
        if a == b:
            continue
        if a.startswith("?"):
            substitution[a] = b
        elif b.startswith("?"):
            substitution[b] = a
        else:
            return None
    return substitution


def apply_substitution(literal: Literal, substitution: dict[str, str]) -> Literal:
    return Literal(literal.predicate, tuple(dereference(x, substitution) for x in literal.args), literal.positive)


def resolve(first: Clause, second: Clause) -> set[Clause]:
    resolvents: set[Clause] = set()
    for left in first:
        for right in second:
            if left.predicate != right.predicate or left.positive == right.positive:
                continue
            substitution = unify(left.args, right.args)
            if substitution is None:
                continue
            remaining = (first - {left}) | (second - {right})
            resolvent = frozenset(apply_substitution(lit, substitution) for lit in remaining)
            # Tautologies cannot help derive a contradiction.
            if not any(
                Literal(lit.predicate, lit.args, not lit.positive) in resolvent
                for lit in resolvent
            ):
                resolvents.add(resolvent)
    return resolvents


def resolution_proves(knowledge_base: list[Clause], query: Literal) -> bool:
    known = set(knowledge_base)
    known.add(frozenset({Literal(query.predicate, query.args, not query.positive)}))
    while True:
        new: set[Clause] = set()
        current = list(known)
        for i, first in enumerate(current):
            for second in current[i:]:
                new.update(resolve(first, second))
        if frozenset() in new:
            return True
        new -= known
        if not new:
            return False
        known.update(new)


def main() -> None:
    # Facts and implications in clause form:
    # HighIncome(John), GoodCredit(John)
    # NOT HighIncome(x) OR NOT GoodCredit(x) OR EligibleForLoan(x)
    knowledge_base = [
        frozenset({Literal("HighIncome", ("John",))}),
        frozenset({Literal("GoodCredit", ("John",))}),
        frozenset({
            Literal("HighIncome", ("?x",), False),
            Literal("GoodCredit", ("?x",), False),
            Literal("EligibleForLoan", ("?x",)),
        }),
    ]
    query = Literal("EligibleForLoan", ("John",))
    print("Query: EligibleForLoan(John)")
    print("Resolution with the negated query:", "proved" if resolution_proves(knowledge_base, query) else "not proved")


if __name__ == "__main__":
    main()
