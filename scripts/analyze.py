import click
import logging
from RecordLib.serializers import to_serializable # DataClassJSONEncoder
from RecordLib.crecord import CRecord
from RecordLib.summary import Summary
from RecordLib.docket import Docket
from RecordLib.analysis import Analysis
from RecordLib.redis_helper import RedisHelper
from RecordLib.ruledefs import (
    expunge_summary_convictions,
    expunge_nonconvictions,
    expunge_deceased,
    expunge_over_70,
    seal_convictions
)
from RecordLib.summary.pdf import parse_pdf as parse_pdf_summary
import pytest
import json
import os
import re
from typing import List

def analyze(summaries: List[Summary], dockets: List[Docket]) -> str:
    """
    Return the analysis of a list of summaries and dockets.
    """
    rec = CRecord()
    [rec.add_summary(s) for s in summaries]
    [rec.add_docket(d) for d in dockets]
    analysis = (
        Analysis(rec)
        .rule(expunge_deceased)
        .rule(expunge_over_70)
        .rule(expunge_nonconvictions)
        .rule(expunge_summary_convictions)
        .rule(seal_convictions)
    )
    return analysis

   


@click.group()
@click.option("--tempdir", "-td", type=click.Path(), default="tests/data/tmp")
@click.option("--redis-collect", "-rc", default=None, type=str, help="connection to redis, in the form [host]:[port]:[db number]:[environment name]. For example, 'localhost:6379:0:development'")
@click.pass_context
def cli(ctx, tempdir: str, redis_collect: str):
    """
    Entrypoint for the `analyze` cli.

    Args:
        tempdir (str): Path to a temporary directory needed for intermediate side effects of parsing
        redis_collect (str): If present, indicates that certain info should be collected into a redis store.
    """
    ctx.obj = dict()
    ctx.obj["tempdir"] = tempdir
    ctx.obj["redis_collect"] = redis_collect
    return


def directory_search(ctx, directory: str):
    """
    Analyze records that relate to a person and are in a directory.

    If a directory only has files, use those files to build a crecord to analyze. 

    If a directory has subdirectories, then look into the subdirectories (recursively) until we find 
    directories that have only files to analyze. 

    The analysis will be stored as json file in the directory next to the files it analyzed.

    Currently makes the pretty lame assumption that docket and summary files will end with '_docket.pdf' or 
    '_summary.pdf'.

    Args:
        ctx: context object from Click.
        directory: (str): Path to a directory.
    """
    print(f"Looking in {directory}")
    subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    if len(subdirs) == 0:
        summaries = [f for f in os.listdir(directory) if re.search("_summary.pdf", f)]
        print("Found summaries:")
        print(summaries)
        dockets = [f for f in os.listdir(directory) if re.search("_docket.pdf", f)]
        print("Found dockets:")
        print(dockets)

        summaries = [parse_pdf_summary(os.path.join(directory, s), tempdir = ctx.obj["tempdir"]) for s in summaries]
        dockets = [Docket.from_pdf(os.path.join(directory, d), tempdir=ctx.obj["tempdir"]) for d in dockets]
        dockets = [d for d,e in dockets]
        analysis = analyze(summaries = summaries, dockets = dockets)
        rec = analysis.rec
        with open(os.path.join(directory, f"{rec.person.last_name}_analysis.json"), "w", encoding="utf8") as f:
            f.write(json.dumps(analysis.analysis, indent=4, default=to_serializable, ensure_ascii=False))
        with open(os.path.join(directory, f"{rec.person.last_name}_record.json"), "w") as f:
            f.write(json.dumps(rec, indent=4, default=to_serializable, ensure_ascii=False))
    else:
        print(f"  Digging deeper...")
        for d in subdirs:
            directory_search(ctx, os.path.join(directory, d))
    return

@cli.command()
@click.pass_context
@click.option("--directory", "-d", type=click.Path(), required=True)
def dir(ctx, directory: str):
    """
    CLI Entrypoint to analyze all the files in a directory containing info about a single person.

    This method just passes along the parameters to directory_search, which does the work.

    """
    directory_search(ctx, directory)    
    return

@cli.command()
@click.option("--pdf-summary", "-ps", type=click.Path(), required=True, default=None)
@click.pass_context
def doc(ctx, pdf_summary: str) -> None:
    """
    Analyze a single file for sealings and expungements. 

    Parse a single file (currently must be a pdf of a summary sheet) and print a json-formatted analysis of
    the record. Optionally save certain anonymous parts of the record to a redis store, to build
    a good catalogue of the kinds of values that variables can have.


    Args:
        pdf_summary (str): Path to a pdf summary
            """
    rec = CRecord()
    if pdf_summary is not None:
        rec.add_summary(parse_pdf_summary(pdf_summary, tempdir = ctx.obj["tempdir"]))

    redis_collect = ctx.obj["redis_collect"]

    if redis_collect is not None:
        try:
            redis_options = redis_collect.split(":")
            rh = RedisHelper(host=redis_options[0], port=redis_options[1],
                             db=redis_options[2],env=redis_options[3])
            rh.sadd_crecord(rec)
        except Exception as e:
            logging.error("You supplied --redis-collect, but collection failed.")

    analysis = (
        Analysis(rec)
        .rule(expunge_deceased)
        .rule(expunge_over_70)
        .rule(expunge_nonconvictions)
        .rule(expunge_summary_convictions)
        .rule(seal_convictions)
    )


    print(json.dumps(analysis.analysis, indent=4, default=to_serializable)) #cls=DataClassJSONEncoder))
