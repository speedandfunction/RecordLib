from __future__ import annotations
from typing import Callable
from RecordLib.crecord import CRecord
import copy
from collections import OrderedDict

class Analysis:
    """
    The Analysis object structures the process of figuring out what can be sealed and expunged from a criminal record. 
    It also helps answer questions about why parts of a criminal record can't be expunged. 

    You initialize an Analysis with a CRecord (which represents someone's criminal record). 
    
    Next, you repeatedly call rule functions on the analysis, using the Analysis.rule method. 
    
    Each rule function evaluates whether certain cases or charges can be sealed or expunged under certain conditions. 
    The rule function separates the cases/charges that meet the rule's conditions from the cases/charges that don't. 

    A CRecord looks like:
        Person
        Cases
            Charges

    The rule function slices the CRecord into two: the slice that meets the rule's conditions, and the slice that doesn't. 
    The slice that _does_ meet the rule's conditions gets wrapped up in a `PetitionDecision.`

    The `PetitionDecision` is a Decision where the `name` describes the issue the rule deals with 
    (e.g. Expungements of nonconvictions); the value is a Petition object representing what petitions the rule decided it could create;
    and the `reasoning` is a tree of `Decisions`

    Each rule function takes a criminal record and returns a tuple of a tree of Decisions and a CRecord. 
    """

    def __init__(self, rec: CRecord) -> None:
        self.record = rec
        self.remaining_record = copy.deepcopy(rec)
        self.decisions = []

    def rule(self, ruledef: Callable) -> Analysis:
        """
        Apply the rule `ruledef` to this analysis. 

        Args:
            ruledef (callable): ruledef is a callable. It takes a `crecord` as the only parameter. 
                It returns a tuple like (CRecord, Decision). The CRecord is whatever cases and charges remain
                on the input CRecord after applying `ruledef`. The Decision is an analysis of the record's
                eligibility for sealing or expungement. The Decision has a plain-langage `name`. It has a `value`
                that is a list of `Petiion` objects. And it has a `reasoning` that is a list of `Decisions` which
                explain how the rule decided what Petitions should be created.

        Returns:
            This Analyis, after applying the ruledef and updating the analysis with the results of the ruledef.
        """
        remaining_record, petition_decision = ruledef(self.remaining_record)
        self.remaining_record = remaining_record
        self.decisions.append(petition_decision)
        return self

