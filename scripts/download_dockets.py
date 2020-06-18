import click
import logging
import requests
import os
from RecordLib.utilities.number_generator import create_docket_numbers
import csv
from ujs_search.services import searchujs
from datetime import datetime

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"


@click.group()
def cli():
    return


def download(url, dest_path, name, doc_type):
    """ Download something from a url """
    resp = requests.get(url, headers={"User-Agent": "DocketAnalyzerTesting"})
    if resp.status_code == 200:
        logging.info(f"Downloaded {doc_type}")
        with open(f"{dest_path}/{name}_{doc_type}.pdf", "wb") as downloaded:
            downloaded.write(resp.content)
    return


<<<<<<< HEAD
def download_docket(scraper_url: str, court: str, docket_number: str, doc_type: str):
    """ Download a single docket using the DocketScraperAPI.
=======
def download_docket(docket_number: str, doc_type: str):
    """ Download a single docket from the UJS portal..
>>>>>>> 4915274440201985511180069552af9aa7c5f4da

    Args:
        docket_number: the docket number.
        doc_type: summary or docket.

    Returns:
        If successful, a tuple with the url of the downloaded file
        as well as the downloaded file. Otherwise, a tuple (None, None)
    """
<<<<<<< HEAD
    resp = requests.post(
        f"{scraper_url}/ujs/search/docket/", json={"docket_number": docket_number}
    )
    if resp.json().get("status") and "Error" in resp.json().get("status"):
        logging.error("Error from ScraperAPI:" + resp.json().get("status"))
        return None, None
    if (
        resp.status_code == 200
        and resp.json().get("searchResults") is not None
        and len(resp.json().get("searchResults")) > 0
    ):
        logging.info("... URL found. Downloading file.")
        if doc_type.lower() in ["s", "summary", "summaries"]:
            # download the summary
            try:
                url = resp.json()["searchResults"][0]["summary_url"]
            except:
                url = None
        else:
            try:
=======
    try:

        resp = searchujs.search_by_docket(docket_number)
    except Exception as e:
        logging.error(str(e))
        return None, None
    if len(resp) > 0:
        logging.info("... URL found. Downloading file.")
        if doc_type.lower() in ["s", "summary", "summaries"]:
            # download the summary
            url = resp[0]["summary_url"]
        else:
            url = resp[0]["docket_sheet_url"]
>>>>>>> 4915274440201985511180069552af9aa7c5f4da

                url = resp.json()["searchResults"][0]["docket_sheet_url"]
            except:
                url = None
        resp = requests.get(url, headers={"User-Agent": "DocketAnalyzerTesting"})
        if resp.status_code == 200:
            logging.info("Docket found and downloaded.")
            return url, resp.content
        else:
            logging.error(
                f"...request for url failed. Status code: { resp.status_code }"
            )
            logging.error(f"   URL was { url }")
<<<<<<< HEAD
        logging.info("... Downloading complete. Moving on.")
=======
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
    else:
        logging.info("No docket found.")

    return None, None


@cli.command()
@click.option("-p", "--dest-path", default="tests/data", show_default=True)
<<<<<<< HEAD
@click.option("-u", "--scraper-url", default="http://localhost:5000", show_default=True)
=======
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
@click.option(
    "-dt",
    "--doc-type",
    default="summary",
    show_default=True,
    type=click.Choice(["summary", "docket", "both"]),
)
@click.option("-i", "--input-csv", required=True)
@click.option("-o", "--output-csv", default=None)
@click.option(
    "-c",
    "--court",
    default="CP",
    show_default=True,
    type=click.Choice(["CP", "MDJ", "both"]),
)
def names(
<<<<<<< HEAD
    dest_path: str,
    scraper_url: str,
    doc_type: str,
    input_csv: str,
    output_csv: str,
    court: str,
=======
    dest_path: str, doc_type: str, input_csv: str, output_csv: str, court: str,
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
) -> None:
    """Download dockets from a list of names.
    TODO need to be able to search both CP and MDJ dockets in one call of this cli.
    """
    logging.basicConfig(level=logging.INFO)

    if court == "CP":
        courts = ["CP"]
    elif court == "MDJ":
        courts = ["MDJ"]
    else:
        courts = ["MDJ", "CP"]

    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)

    with open(input_csv, "r") as input_file:
        reader = csv.DictReader(input_file)
        if output_csv:
            output_file = open(output_csv, "a+")
            writer = csv.DictWriter(
                output_file, reader.fieldnames + ["Name", "DOB", "url", "doctype"]
            )
        if "Name" not in reader.fieldnames or "DOB" not in reader.fieldnames:
            logging.error("Input-file must have the columns 'Name' and 'DOB'")
            return

        for row in reader:
            name = row["Name"].split(" ")
            first_name = name[0]
            last_name = name[-1]
            dob = datetime.strptime(row["DOB"], r"%m/%d/%Y")
            for court_to_search in courts:
<<<<<<< HEAD
                resp = requests.post(
                    f"{scraper_url}/searchName/{court_to_search}",
                    json={
                        "first_name": first_name,
                        "last_name": last_name,
                        "dob": row["DOB"],
                    },
                )
                if resp.status_code == 200:
                    logging.info(f"Successful search for {row['Name']}")
                    if doc_type.lower() in ["s", "summary", "summaries", "both"]:
                        # download the summary
                        try:
                            logging.info("... Downloading summary")
                            row["url"] = resp.json()["dockets"][0]["summary_url"]
                            row["doctype"] = "summary"
                            if output_csv:
                                writer.writerow(row)
                            download(row["url"], dest_path, row["Name"], doc_type)
                        except:
                            logging.error(f"... No summary found for {row['Name']}.")
                            row["url"] = ""
                            row["doctype"] = "none"
=======
                results = searchujs.search_by_name(
                    first_name, last_name, dob, court=court_to_search
                )
                if len(results[court_to_search]) > 0:
                    logging.info(f"Successful search for {row['Name']}")
                    if doc_type.lower() in ["s", "summary", "summaries", "both"]:
                        # download the summaries
                        for result in results[court_to_search]:
                            try:
                                logging.info("... Downloading summary")
                                row["url"] = result["summary_url"]
                                row["doctype"] = "summary"
                                if output_csv:
                                    writer.writerow(row)
                                download(row["url"], dest_path, row["Name"], "summary")
                            except:
                                logging.error(
                                    f"... No summary found for {row['Name']}."
                                )
                                row["url"] = ""
                                row["doctype"] = "none"
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
                    if doc_type.lower() in ["d", "docket", "both"]:
                        logging.info("... Downloading dockets")
                        for i, result in enumerate(results[court_to_search]):
                            try:
                                row["url"] = result["docket_sheet_url"]
                                row["doctype"] = "docket"
                                if output_csv:
                                    writer.writerow(row)
                                download(
                                    row["url"],
                                    dest_path,
                                    row["Name"] + "_" + str(i),
<<<<<<< HEAD
                                    doc_type,
                                )
                        except:
                            logging.error(f" No dockets found for {row['Name']}.")
                            row["url"] = ""
                            row["doctype"] = "none"
=======
                                    "docket",
                                )
                            except:
                                logging.error(f" No dockets found for {row['Name']}.")
                                row["url"] = ""
                                row["doctype"] = "none"
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
                else:
                    logging.warning(f"Did not find any results for {row['Name']}")
                if output_csv:
                    writer.writerow(row)

    if output_csv:
        output_file.close()
    logging.info("Complete.")
    return


@cli.command()
@click.option("-dn", "--docket-number", required=True)
@click.option(
    "-dt",
    "--doc-type",
    default="summary",
    show_default=True,
    type=click.Choice(["summary", "docket"]),
)
@click.option("-o", "--output", required=True)
def docket_number(docket_number: str, doc_type: str, output: str):
    url, resp_content = download_docket(docket_number, doc_type)
    if resp_content is not None:
        click.echo("Downloaded docket.")
        with open(output, "wb") as f:
            f.write(resp_content)
        click.echo(f"Saved docket to {output}")


@cli.command()
@click.option("-p", "--dest-path", default="tests/data", show_default=True)
<<<<<<< HEAD
@click.option("-u", "--scraper-url", default="http://localhost:5000", show_default=True)
=======
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
@click.option(
    "-dt",
    "--doc-type",
    default="summary",
    show_default=True,
    type=click.Choice(["summary", "docket"]),
)
@click.option("-i", "--input-csv", required=True)
@click.option("-o", "--output-csv", default=None)
<<<<<<< HEAD
def docket_numbers(
    dest_path: str, scraper_url: str, doc_type: str, input_csv: str, output_csv: str
=======
def docket_number_file(
    dest_path: str, doc_type: str, input_csv: str, output_csv: str
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
) -> None:
    """
    Download dockets or summary sheets for the docket numbers listed in <input-csv>

    You need to have the DocketScraperAPI running at <scraper-url>
    """
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)
    with open(input_csv, "r") as input_file:
        if output_csv:
            output_file = open(output_csv, "a+")
            writer = csv.DictWriter(output_file, ["Docket Number", "url"])
        reader = csv.DictReader(input_file)
        if "Docket Number" not in reader.fieldnames:
            logging.error("Input-file must have the column 'Docket Number'")
            return
        for row in reader:
            docket_number = row["Docket Number"]
            court = "CP" if "CP-" in docket_number else "MDJ"
<<<<<<< HEAD
            url, resp_content = download_docket(
                scraper_url, court, docket_number, doc_type
            )
=======
            url, resp_content = download_docket(docket_number, doc_type)
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
            if resp_content is not None:
                with open(
                    os.path.join(dest_path, f"{ docket_number }_{ doc_type }.pdf"),
                    "wb",
                ) as f:
                    f.write(resp_content)
                    row["url"] = url
                    if output_csv:
                        writer.writerow(row)
            else:
                logging.error(f"Could not find {docket_number}.")
        if output_csv:
            output_file.close()
        logging.info("Complete.")


@cli.command()
@click.argument("DOCUMENT_TYPE")
@click.option("--number", "-n", default=1, show_default=True)
@click.option("--dest-path", default="tests/data", show_default=True)
@click.option("--court", default="CP", type=click.Choice(["CP", "MDJ", "either"]))
def random(document_type: str, number: int, dest_path: str, court: str) -> None:
    """
    Download <n> random "summary" documents or "docket" documents to <dest-path>.

    You need to have the DocketScraperAPI running at <scraper-url>
    """
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)

    for _ in range(number):
        docket_number = next(create_docket_numbers(court))
        logging.info(f"Finding { docket_number } ... ")
        if court == "either":
            court_to_search = "CP" if "CP-" in docket_number else "MDJ"
            logging.info("court is now " + court_to_search)
        else:
            court_to_search = court
<<<<<<< HEAD

        _, resp_content = download_docket(
            scraper_url, court_to_search, docket_number, document_type
        )
=======
        url_to_fetch, resp_content = download_docket(docket_number, document_type)
>>>>>>> 4915274440201985511180069552af9aa7c5f4da
        if resp_content is not None:
            with open(
                os.path.join(dest_path, f"{ docket_number }_{ document_type }.pdf"),
                "wb",
            ) as f:
                f.write(resp_content)

    logging.info("Complete.")


@cli.command()
@click.option("--url-file", "-u", type=click.Path())
@click.option("--dest-dir", "-dd", type=click.Path())
@click.option("--nest-dirs/--no-nest-dirs", default=True)
def urls(url_file: str, dest_dir: str, nest_dirs: bool):
    """
    Download documents given a table that contains their urls. 
    
    Args:
        url_file: path to csv file listing urls of documents to download.
        dest_dir: path to directory where downloaded dockets should go.
        nest_dirs: Should the downloaded documents each get put inside their own subdirectory? Default True.
    """
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(dest_dir):
        logging.warning(f"{dest_dir} does not already exist. Creating it")
        os.mkdir(dest_dir)

    with open(url_file, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["name", "url", "type"]
        for row in reader:
            person_name = row["name"].replace(" ", "_")
            if nest_dirs:
                file_dest = os.path.join(dest_dir, person_name)
                if not os.path.exists(file_dest):
                    os.mkdir(file_dest)
            else:
                file_dest = dest_dir
            download(row["url"], file_dest, person_name, row["type"])
<<<<<<< HEAD
=======

>>>>>>> 4915274440201985511180069552af9aa7c5f4da
