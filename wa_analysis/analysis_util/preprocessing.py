"""Module for text preprocessing
"""
import re
from functools import partial
import pandas as pd
from wa_analysis.analysis_util import processing_meta as pm
from wa_analysis.optimization_services import optimization_services as opts

# Process meta-configuration data pm.processing_by_re_meta
# li_processing: List of text objects to be processed
# li_processing_re_capture: List of text objects to be processed and captured
li_processing_re = []
li_processing_re_capture = []
for text_obj, meta_dict in pm.processing_by_re_meta.items():
    li_processing_re.append(text_obj)
    if meta_dict["capture"]:
        li_processing_re_capture.append(text_obj)


class TextCleaning:
    """Class for Cleaning Text"""

    def __init__(self, text: str) -> None:
        self.text = text

    def convert_text_to_lower_case(self) -> str:
        """Convert to lower case"""
        return self.text.lower()

    @staticmethod
    def _re_sub_replace(
        text: str, pattern: str, replacement_str: str, flags, capture: bool
    ) -> dict[str, list[str]]:
        """Service for pattern replacement"""
        re_compiled = re.compile(pattern, flags=flags)
        if capture:
            matches = re_compiled.findall(text)
        else:
            matches = []
        return dict(text=re_compiled.sub(replacement_str, text), matches=matches)

    def convert_in_text(self, text_object: str):
        """Convert certain object in text.
        Configuration is provided in processing_meta
        """
        assert (
            text_object in pm.processing_by_re_meta.keys()  # pylint: disable=C0201
        ), "Conversion for the chosen object has not yet been implemented"

        _temp_input = pm.processing_by_re_meta[text_object]
        _temp_input["text"] = self.text

        return self._re_sub_replace(**_temp_input)["text"]

    def clean_text(self) -> str:
        """
        process the text
        """
        # Convert to lower case
        self.text = self.convert_text_to_lower_case()

        for step in li_processing_re:
            self.text = self.convert_in_text(text_object=step)

        # trim
        self.text = self.text.strip("'\"")
        return self.text

    def convert_capture_in_text(self, text_object: str) -> dict[str, dict[str, str]]:
        """Convert certain object in text.
        Configuration is provided in processing_meta
        """

        assert (
            text_object in pm.processing_by_re_meta.keys()  # pylint: disable=C0201
        ), "Conversion for the chosen object has not yet been implemented"
        _temp_input = pm.processing_by_re_meta[text_object]
        _temp_input["text"] = self.text
        _result = self._re_sub_replace(**_temp_input)
        return {"text": _result["text"], text_object: _result["matches"]}

    def clean_capture_text(self) -> tuple[str, dict]:
        """Clean text from certain objects and capture those

        Returns:cleaned string and dict with corresponding object
        """
        _result = dict.fromkeys(["text", "url", "at_user", "hash_tag"])

        for step in li_processing_re:
            _result_step = self.convert_capture_in_text(text_object=step)
            self.text = _result_step["text"]
            if pm.processing_by_re_meta[step]["capture"]:
                _result[step] = _result_step[step]

        _result["text"] = self.text
        return _result


def clean_capture_text(text: str) -> tuple[str, dict]:
    """Function for text cleaning

    Args:
        text (str): input text

    Returns:
        tuple[str,dict]: tuple with cleaned text, and captures
    """
    return TextCleaning(text).clean_capture_text()


class TextCleaningDF:
    """Class for cleaning text column in a DF"""

    def __init__(self, df_input: pd.DataFrame, col_txt: str, in_parallel=False):
        self.df_input = df_input
        self.col_txt = col_txt
        self.in_parallel = in_parallel

        self.col_result = "result"
        self.df_output = pd.DataFrame()

    @staticmethod
    def _clean_capture_text_df(
        df_input: pd.DataFrame, col_txt: str, col_result: str
    ) -> pd.DataFrame:
        """Clean capture text on text column in df
        and write a result dict to a result column (col_result)
        """
        _df_temp = df_input
        _df_temp[col_result] = _df_temp[col_txt].apply(clean_capture_text)
        return _df_temp

    def clean_capture_text_df(self) -> pd.DataFrame:
        """Clean capture text on text column in df and write the corresponding result columns"""
        if not self.in_parallel:
            self.df_output = self._clean_capture_text_df(
                self.df_input, self.col_txt, self.col_result
            )
        else:
            self.df_output = opts.execute_in_parallel(
                partial(
                    self._clean_capture_text_df,
                    col_txt=self.col_txt,
                    col_result=self.col_result,
                )
            )(self.df_input)
        self.df_output[[self.col_txt] + li_processing_re_capture] = self.df_output[
            self.col_result
        ].apply(pd.Series)
        return self.df_output


def clean_capture_text_df(
    df_input: str, col_txt: str, in_parallel=False
) -> pd.DataFrame:
    """Function for cleaning text column in a DF"""
    return TextCleaningDF(
        df_input=df_input, col_txt=col_txt, in_parallel=in_parallel
    ).clean_capture_text_df()
