"""
Classes representing expungment or sealing petitions. 

TODO These are really just stubs for now while I'm working on what the Analysis and ruledef function signatures look like.
"""
from RecordLib.case import Case
from RecordLib.attorney import Attorney
from RecordLib.common import Person
from typing import Optional, List
from docxtpl import DocxTemplate
import io 
from datetime import date

class Petition:

    def __init__(self, attorney: Optional[Attorney] = None, client: Optional[Person] = None, cases: Optional[List[Case]] = None) -> None:
        self.attorney = attorney
        self.cases = cases or []
        self.client = client
        self._template = None

    def set_template(self, template_file: io.BytesIO) -> None:
        self._template = DocxTemplate(template_file)

    def add_case(self, case: Case) -> None:
        self.cases.append(case)


    def render(self) -> DocxTemplate:
        """
        Return the filled-in template document.
        """
        raise NotImplementedError

    def __repr__(self):
        return (f"Petition(Client: {self.client}, Cases: {[c for c in self.cases]})")

class Expungement(Petition):
    # class-level constants for the type of the expungment. FULL/Partial is only relevant to 
    # helping the user understand what this expungement is.
    FULL_EXPUNGEMENT = "Full Expungement"
    PARTIAL_EXPUNGEMENT = "Partial Expungement"
    

    # Class constants for the section of the PA Criminal Procedure rules, pursuant to which this
    # expungement is being filed. 
    # 490 is for expunging summary convictions,
    # 790 is for expunging everything else. 
    SUMMARY_EXPUNGEMENT = "§ 490"
    NONSUMMARY_EXPUNGEMENT = "§ 790"

    def __init__(self, *args, **kwargs):
        if "type" in kwargs.keys():
            self.type = kwargs["type"]
            kwargs.pop("type")
        else: 
            self.type = ""


        if "procedure" in kwargs.keys():
            self.procedure = kwargs["procedure"]
            kwargs.pop("procedure")
        else:
            self.procedure = ""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return (f"Petition({self.type}, Client: {self.client}, Cases: {[c for c in self.cases]})")

    def render(self) -> DocxTemplate:
        """
        Return the filled-in template document.
        """
        self._template.render({
            "date": date.today().strftime(r"%B %d, %Y"),
            "petition_type": "Expungement",
            "petition_procedure": self.procedure,
            "attorney": self.attorney, 
            "client": self.client, 
            "cases": self.cases,
            "ifp_message": r"{{IFP MESSAGE NOT IMPLEMENTED YET}}",
            "summary_extra": "EXTRA SUMMARY STUFF" if self.procedure == Expungement.SUMMARY_EXPUNGEMENT else "",
            "service_agencies": []})
        return self._template


class Sealing(Petition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)