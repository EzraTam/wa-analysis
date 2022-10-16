"""Module for analyzing WA DF
"""

import os
import re
import pandas as pd


def extract_emoji(text: str) -> dict:
    """Extract emojis from text and delete them"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )

    return dict(text=emoji_pattern.sub(r"", text), emojis=emoji_pattern.findall(text))


def extract_emoji_df(df_input: pd.DataFrame, col_text: str) -> pd.DataFrame:
    """From a DF with text column extract the emoji out of the text in the column

    Args:
        df (pd.DataFrame): DF containing text column to be processed
        col_text (str): Name of the text column

    Returns:
        pd.DataFrame: _description_
    """
    df_input["emoji_extracted"] = df_input[col_text].apply(extract_emoji)
    df_input = df_input.drop(columns=[col_text])
    df_input[[col_text, "emojis"]] = df_input["emoji_extracted"].apply(pd.Series)
    df_input = df_input.drop(columns=["emoji_extracted"])
    return df_input


################################
###Get Feature Vector
################################

# start replaceTwoOrMore
def replace_two_or_more(text: str) -> str:
    """look for 2 or more repetitions of character and replace with the character itself"""
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", text)


# start getStopWordList
def load_stop_word_list(stop_word_list_path: str) -> str:
    """read the stopwords file and build a list"""
    stop_words = []
    stop_words.append("AT_USER")
    stop_words.append("URL")

    with open(stop_word_list_path, "r", encoding="utf-8") as file:
        line = file.readline()
        while line:
            word = line.strip()
            stop_words.append(word)
            line = file.readline()

    return stop_words


def get_feature_vector(text: str, stop_words: list) -> list:
    """Extract feature vector from a text

    Args:
        text (str): input text
        stop_words (list): list of stop words

    Returns:
        list: Array of feature vector
    """
    feature_vector = []
    # split tweet into words
    list_words = text.split()
    for word in list_words:
        # replace two or more with two occurrences
        word = replace_two_or_more(word)
        # strip punctuation
        word = word.strip("'\"?,.")
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word)
        # ignore if it is a stop word
        if word in stop_words or val is None:
            continue
        else:
            feature_vector.append(word.lower())
    return feature_vector


## Emoji Analysis

# Load sentiment table and normalize
sentiment_table = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "data", "ijstable.csv")
)
li_col_norm = ["Negative", "Neutral", "Positive"]
for col in li_col_norm:
    sentiment_table[col] = sentiment_table[col] / sentiment_table["Occurrences"]


def extract_emoji_sentiment(emoji: str) -> dict[float, float, float]:
    """Extract sentiment from an emoji

    Args:
        emoji (str): input emoji

    Returns:
        dict[float,float,float]: Sentiment dict
    """
    res = sentiment_table[sentiment_table.Emoji == emoji]
    if not res.empty:
        return dict(
            neg=float(res["Negative"].values[0]),
            neut=float(res["Neutral"].values[0]),
            pos=float(res["Positive"].values[0]),
        )
    else:
        return dict(neg=0, neut=0, pos=0)


def extract_emoji_sentiment_from_list(emoji_list: list) -> dict[float, float, float]:
    """Extract sentiment from emoji list. Done by averaging the sentiment score of each emoji

    Args:
        emoji_list (list): List of emojis

    Returns:
        dict[float,float,float]: Sentiment score
    """
    val = dict(neg=[], neut=[], pos=[])
    for emoji in emoji_list:
        for sent, value in extract_emoji_sentiment(f"{emoji}").items():
            val[sent].append(value)

    for sent in val.keys():  # pylint: disable=C0201
        val[sent] = sum(val[sent]) / len(val[sent])
    return val
