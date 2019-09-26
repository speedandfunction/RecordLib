import io

from RecordLib.petitions import Petition, Expungement, Sealing


def test_petition(example_attorney, example_person, example_case):
    p = Petition(attorney=example_attorney, client=example_person, cases=[example_case])
    assert p.cases[0] == example_case

def test_file_name(example_attorney, example_person, example_case):
    p = Petition(attorney=example_attorney, client=example_person, cases=[example_case])
    assert p.file_name() == "GenericPetition_" + example_person.last_name + "_" + example_case.docket_number + ".docx"

# EXPUNGEMENT PETITIONS
def test_expungement_petition(example_attorney, example_person, example_case):
    p = Expungement(attorney=example_attorney, client=example_person, cases=[example_case], 
                    expungement_type=Expungement.ExpungementTypes.FULL_EXPUNGEMENT,
                    procedure=Expungement.ExpungementProcedures.NONSUMMARY_EXPUNGEMENT)
    assert p.cases[0] == example_case
    assert p.expungement_type == Expungement.ExpungementTypes.FULL_EXPUNGEMENT
    assert p.procedure == Expungement.ExpungementProcedures.NONSUMMARY_EXPUNGEMENT

def test_render_expungement_petition(example_person, example_attorney, example_case): 
    p = Expungement(attorney=example_attorney, client=example_person, cases=[example_case], 
                    expungement_type=Expungement.ExpungementTypes.FULL_EXPUNGEMENT)
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", "rb") as doc:
        p.set_template(doc)

    doc = p.render()
    # breakpoint()
    # use doc.save() to manually inspect the rendered petition.
    assert "docx" in doc.__dict__.keys()

# SEALING PETITIONS
def test_sealing_petition(example_person, example_case):
    p = Sealing(client=example_person, cases=[example_case])
    assert p.cases[0] == example_case
