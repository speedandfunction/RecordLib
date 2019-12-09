from grades.models import ChargeRecord
from typing import Dict, List, Tuple
from collections import defaultdict

def match(a: ChargeRecord, b: ChargeRecord) -> bool:
    if a.offense == b.offense and a.section == b.section and a.subsection == b.subsection:
        return True
    return False

def guess_grade(target: ChargeRecord, records: List[ChargeRecord]) -> Tuple[str,float]:
    """
    Guess the grade of an offense.

    Returns:
        A dictionary with each possible grade, and the probability that the `target` charge has that grade.
    """
    weights = defaultdict(lambda: 0)
    for rec in records:
        if match(target, rec):
            weights[rec.grade] += rec.weight
    total_weight = sum([w for g,w in weights.items()])
    probabilities = sorted([
        (g, (w / total_weight))
        for g,w in weights.items()
    ], key=lambda i: i[1])
    return probabilities