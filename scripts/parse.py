import click
from RecordLib.sourcerecords.docket import Docket
from RecordLib.utilities.serializers import to_serializable
import json

@click.command()
@click.option("--doctype", required=True, type=click.Choice(["summary","docket"]))
@click.option("--court", required=False, default=None)
@click.argument("path")
def parse(path, doctype, court):
    """
    Parse a pdf file. Probably only useful for testing.
    """
    if doctype == "summary":
        print("Not implemented yet")
    elif doctype == "docket":
        d, errs = Docket.from_pdf(path, court=court)
        print("---Errors---")
        print(errs)
        print("---Person---")
        print(json.dumps(d._defendant, default=to_serializable))
        print("---Case---")
        print(json.dumps(d._case, default=to_serializable))
    print("Done.") 