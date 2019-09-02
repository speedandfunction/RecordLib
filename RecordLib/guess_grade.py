from RecordLib.common import Charge
from typing import Tuple
import mysql.connector
import os

def int_or_float(n: float) -> Union[int, float]:
    """
    Return a number an int, if it can be an int, else a float.

    For example, 10.0 is returned as 10, but 10.3 returns as 10.3.
    """
    if int(n) == n: return int(n)
    return n

def guess_grade(ch: Charge) -> Tuple[str, float]:
    """
    Guess the grade of a charge.

    Args:
    ch (Charge): A criminal Charge.

    Returns:
    A tuple: (a string indicating the most likely grade of the offense, probability of that grade)
    """
    if ch.get_statute_section() == "" or ch.get_statute_chapter() == "":
        return ("Unknown", 1)
    cnx = mysql.connector.connect(user=os.environ['mysql_user'], password=os.environ['mysql_pw'],
                              host=os.environ['mysql_host'],
                              database='cpcms_aopc_summary')
    cur = cnx.cursor()
    chapter = int_or_float(ch.get_statute_chapter())
    if ch.get_statute_subsections() != "":
        # If the statute doesn't have a subsection, then query the table without subsections.
        query = ("SELECT SUM(Percent) as P FROM crimes_wo_subsection WHERE title='%s' AND section='%s'")
        cur.execute(query, (chapter, ch.get_statute_section()))
    else:
        query = ("SELECT SUM(Percent) as P FROM crimes_w_subsection WHERE title='%s' AND section='%s' " +
                 "AND subsection like '%s%'")
        cur.execute(query, (ch.get_statute_chapter(), c.get_statute_section(), c.get_statute_subsections()))
    breakpoint()
    return ("", 0)
