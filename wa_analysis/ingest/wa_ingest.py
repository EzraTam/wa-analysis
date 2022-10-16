""" Module for ingesting WA Data
"""

import pandas as pd
from wa_analysis import utils as ut


def extract_data(path_conversation: str) -> list:
    """Function for extracting data in list for each conversation

    Args:
        path_conversation (str): Path of the raw data

    Returns:
        list: list containing each conversation in form (data,time,author,message)
    """
    data = []
    with open(path_conversation, encoding="utf-8") as file:
        # Beginning only contains WA information
        file.readline()
        message_buffer = []
        date, time, author = None, None, None
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip("\u200e")

            if ut.check_invisible_pic(line):
                line = line.lstrip("\u200e")

            if ut.date_time(line)["exists"]:
                if len(message_buffer) > 0:
                    data.append([date, time, author, " ".join(message_buffer)])
                message_buffer.clear()
                date, time, author, message = ut.getDatapoint(line)
                message_buffer.append(message.strip())
            else:
                message_buffer.append(line)
    return data


def create_df_from_data(data: list) -> pd.DataFrame:
    """Create DF from list of columns provided by extract data

    Args:
        data (list): list containing the rows

    Returns:
        pd.DataFrame: Resulting DF
    """
    df_temp = pd.DataFrame(data, columns=["date", "time", "author", "message"])
    df_temp["date"] = pd.to_datetime(df_temp["date"], yearfirst=False, dayfirst=True)
    df_temp["time"] = pd.to_datetime(df_temp["time"], format="%H:%M:%S").dt.time
    return df_temp.astype({"time": "string", "author": "string", "message": "string"})


def wa_ingest(path_conversation: str) -> pd.DataFrame:
    """Function to create DF from raw data

    Args:
        path_conversation (str): Path of raw data

    Returns:
        pd.DataFrame: resulting DF
    """
    return create_df_from_data(extract_data(path_conversation))
