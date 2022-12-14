"""Utils for Ingest
"""
from functools import partial
import regex


def pattern_exists(string: str, pattern: str, func):
    """Function to check whether pattern exists

    Args:
        string (str): input string
        pattern (str): pattern to be found in a string
        func (_type_): search function, from regex

    Returns:
        _type_: _description_
    """
    result = {}
    result["match"] = func(pattern, string)
    result["exists"] = False
    if result["match"]:
        result["exists"] = True
    return result


# List of search functions generated by pattern_exists

# Function to search date time of the form [[day].[month].[year-2digit], [hour]:[minute]:[seconds]]
# e.g., [11.12.22, 07:02:11]
date_time = partial(
    pattern_exists,
    pattern=r"\[(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|[1][0-2])\.[0-9]+,\s(0?[0-9]|1[0-9]|2[0-3]):(0?[0-9]|[1-5][0-9]):(0?[0-9]|[1-5][0-9])\]",
    func=regex.match,
)

# Function to search author. Pattern is ] author:
find_author = partial(pattern_exists, pattern="]\s.*:", func=regex.findall)


# Function


def get_date_time_author(string: str):
    """Extract the date, time, and author part in text.
    String to extract:
    [[day].[month].[year-2digit], [hour]:[minute]:[seconds]] [author]:
    """

    return ":".join(string.split(":")[:3]) + ":"


def get_date_time(string_input: str):
    """Get date and time from string wa input"""

    if date_time(string_input)["exists"]:
        date_and_time = (
            date_time(string_input)["match"].group(0).lstrip("[").rstrip("]").split(",")
        )
        date_and_time[1] = date_and_time[1].lstrip()
        date = date_and_time[0]
        time = date_and_time[1]

        return date, time
    else:
        return None


def get_author(string_input: str):
    """Get author name"""
    if find_author(string_input)["exists"]:
        return find_author(string_input)["match"][0].lstrip("] ").rstrip(":")
    else:
        return None


def get_message(string_input: str) -> str:
    """String has to be of the form [date, time] author: message
    Args:
        string_input (str): input string

    Returns:
        str: message string
    """
    return ":".join(string_input.split(":")[3:]).lstrip()


def check_invisible_pic(input_string: str):
    """Check whether invisible picture exists in string"""
    pattern = "\u200e"
    match = regex.match(pattern, input_string)
    if match:
        return True
    else:
        return False


def getDatapoint(line):
    date, time = get_date_time(line)

    year = date.split(".")[2]
    year = "20" + year

    date = date.split(".")[:2]
    date.append(year)
    date = ".".join(date)

    author = get_author(get_date_time_author(line))
    message = get_message(line)
    return date, time, author, message
