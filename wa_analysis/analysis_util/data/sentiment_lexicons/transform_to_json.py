import os
import json

import csv

path_data=os.path.dirname(__file__)

li_files=["sentiment_negative_scores","sentiment_positive_scores"]

for file_nm in li_files:

    with open(os.path.join(path_data,f"{file_nm}.tsv"),encoding="utf-8") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        next(tsv_file, None)

        dict_sent={key:int(value) for (key,value) in tsv_file}


    with open(os.path.join(path_data,f"{file_nm}.json"), 'w',encoding="utf-8") as fp:
        json.dump(dict_sent, fp)
