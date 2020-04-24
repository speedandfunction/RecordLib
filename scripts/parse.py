import click
from RecordLib.sourcerecords.docket import Docket
from RecordLib.utilities.serializers import to_serializable
import json
import logging
import sys


@click.command()
@click.option("--doctype", required=True, type=click.Choice(["summary","docket"]))
@click.option("--court", required=False, default=None)
@click.option("--loglevel","-l", required=False, default="DEBUG")
@click.argument("path")
def parse(path, doctype, court, loglevel):
    """
    Parse a pdf file. Probably only useful for testing.
    """
    root_logger  = logging.getLogger() # create root logger that submodules will inherit
    root_logger.setLevel(loglevel)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
    handler.setLevel(loglevel)
    root_logger.addHandler(handler)
    root_logger.info("Logging is working")
    if doctype == "summary":
        click.echo("Not implemented yet")
    elif doctype == "docket":
        d, errs = Docket.from_pdf(path, court=court)
        click.echo("---Errors---")
        click.echo(errs)
        click.echo("---Person---")
        click.echo(json.dumps(d._defendant, default=to_serializable, indent=4))
        click.echo("---Case---")
        click.echo(json.dumps(d._case, default=to_serializable, indent=4))
    click.echo("Done.") 