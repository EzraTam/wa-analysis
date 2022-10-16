"""Module for optimizing performances
of computing such as paralellization
"""

import concurrent.futures
import numpy as np
import psutil
import pandas as pd


def execute_in_parallel(func):
    """Decorator for excuting parallel computation for a function on a dataframe
    with available number of cores

    Args:
        func (function): function to compute
    """

    def inner(df_input: pd.DataFrame) -> pd.DataFrame:
        df_results = []
        logical = False
        num_procs = psutil.cpu_count(logical=logical)
        splitted_df = np.array_split(df_input, num_procs)
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_procs) as executor:
            results = [executor.submit(func, df_input=df) for df in splitted_df]
            for result in concurrent.futures.as_completed(results):
                try:
                    df_results.append(result.result())
                except Exception as ex:  # pylint: disable=broad-except
                    print(str(ex))
        return pd.concat(df_results).sort_index()

    return inner
