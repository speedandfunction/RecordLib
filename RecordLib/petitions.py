"""
Classes representing expungment or sealing petitions. 

TODO These are really just stubs for now while I'm working on what the Analysis and ruledef function signatures look like.
"""
from RecordLib.case import Case
from RecordLib.attorney import Attorney
from RecordLib.person import Person
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

    def file_name(self) -> str:
        """
        Return a file name for the rendered petition.
        """
        try:
            docknum = cases[0].docket_number 
        except:
            docknum = "NoCases"
        return f"GenericPetition_{self.client.last_name}_{self.cases[0].docket_number}.docx"

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
    class ExpungementTypes:
        FULL_EXPUNGEMENT = "Full Expungement"
        PARTIAL_EXPUNGEMENT = "Partial Expungement"
    

    # Class constants for the section of the PA Criminal Procedure rules, pursuant to which this
    # expungement is being filed. 
    # 490 is for expunging summary convictions,
    # 790 is for expunging everything else. 
    class ExpungementProcedures:
        SUMMARY_EXPUNGEMENT = "§ 490"
        NONSUMMARY_EXPUNGEMENT = "§ 790"

    petition_type="Expungement"

    def __init__(self, *args, **kwargs):
        if "expungement_type" in kwargs.keys():
            self.expungement_type = kwargs["expungement_type"]
            kwargs.pop("expungement_type")
        else: 
            self.expungement_type = ""


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
            "summary_extra": "EXTRA SUMMARY STUFF" if self.procedure == Expungement.ExpungementProcedures.SUMMARY_EXPUNGEMENT else "",
            "service_agencies": []})
        return self._template


class Sealing(Petition):

    petition_type = "Sealing"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)