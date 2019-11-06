import pandas as pd
import numpy as np
import random
from definitions import *

tickets = pd.read_csv("dataset/tickets.csv")
editors = pd.read_csv("dataset/editors.csv")
editors.rename({"Unnamed: 0": 'No'}, axis='columns', inplace=True)

def synth_lps_data(editors, lps, max_pairs=1):
    """
    Creates language pairs column with list of language pairs from given editor randomly selected from language pairs on
    tickets, whit random size between 1 and max_pairs
    :param editors: pandas Dataframe with editors database.
    :param lps: list of unique language pairs on tickets database
    :param max_pairs: int, max number of language pairs to generate per editor. To maintain the simplicity of the
    challenge is set to 1. Assuming that if a given editor masters more than one LP, another id is created.
    """
    editors['language_pairs'] = editors.apply(lambda x: random.sample(lps, random.randint(1, max_pairs)), axis=1)


# def synth_skill_by_lps_data(editors, lps):
#     """
#     Idealized for when the language pair per editor is more than 1.
#     :param editors: pandas Dataframe, w/ editors database w/ language pairs info.
#     """
#     for lp in lps:
#         lp_domains= [domain+ '_' + lp for domain in domains]
#         for lp_domain in lp_domains:
#             editors[lp_domain] = editors.loc[pd.DataFrame(editors['language_pairs'].to_list()).isin([lp_domain]).any(1), :]\
#                 .apply(lambda x: random.randint(1, 5))
#             editors[lp_domain].fillna(0, inplace=True)
#             # editors.loc[editors['language_pairs'].isin(lp_domain)] = editors.apply(lambda x: random.randint(1, 5))
#         # editors = editors.reindex(editors.columns + pd.Index(lp_cols), axis='columns')

