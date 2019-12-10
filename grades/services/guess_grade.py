import logging
from grades.models import ChargeRecord
from typing import Dict, List, Tuple
from collections import defaultdict

logger = logging.getLogger(__name__)

def match(a: ChargeRecord, b: ChargeRecord) -> bool:
    if a.title == b.title and a.section == b.section and a.subsection == b.subsection:

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
    return sorted(probabilities, key=lambda g: g[1])


def grade_probability(grade: str, gradelist: Tuple[str, float]) -> float:
    """
    Given a list of grades and probabilities, like created from 'guess_grade', return the probability
    of the grade.

    If 'guess_grade' didn't find any probability for a grade, the grade won't be in the grade list at all.
    This utility will tell you the probability of the grade is 0, rather than just throwing an error.
    """
    possibilities = list(filter(lambda g: g[0] == grade, gradelist))
    if len(possibilities) == 0:
        return 0
    if len(possibilities) == 1:
        return possibilities[0][1]
    logger.warn("grade_probabiltity found multiple possibilties in:")
    logger.warn(gradelist)
    logger.warn(grade)
    return possibilities[0][1]