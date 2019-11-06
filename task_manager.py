import pandas as pd
import numpy as np
from definitions import *
import synth_data as synth
import editor_manager as editor_manager
import ticket_manager as ticket_manager
from task_generator import message_producer as msg_producer


def get_prices(task, editors, by_lp=False):
    """
    Determines the price of a given task, if it's performed by the given editor
    :param task: pandas Dataframe row, with task info (number_words, language_pair?, domain)
    :param editors: pandas Dataframe, with editors' info (domain's skill, language pairs??)
    :param by_lp: boolean, set to True if language pairs per editor can be greater than one, and there are columns
    denoting domain skill by language pair.
    # TODO: check this language pair thing
    :return: pandas Dataframe with price estimation for each editor
    """
    lpt = task['language_pair']  #.values[0]
    task_id = task['id']  #.values[0]
    domain = task['domain']  #.values[0]
    if by_lp:
        editors['tmp_task_skills'] = editors[[col for col in editors.columns if lpt in col and domain in col]]
    else:
        # It is assumed tha the domain skills refer to the only language pair from the editor
        editors['tmp_task_skills'] = editors[[col for col in editors.columns if domain in col]]

    # Case LPT in LPE
    editors.loc[pd.DataFrame(editors['language_pairs'].to_list()).isin([lpt]).any(1), 'price_'+ task_id] \
        = alpha * task['number_words_task'] * editors['tmp_task_skills']

    # Case LPT not in LPE
    editors['price'].fillna(0, inplace=True)
    # editors.loc[editors['price_'+ task_id].isna(), 'price_'+ task_id]\
    #     = task['number_words_task'] * np.log(Gamma + editors[editors['price_'+ task_id].isna()]['tmp_task_skills'])

    # remove aux column
    editors.drop('tmp_task_skills', axis=1
                 , inplace=True)

    return editors[['id', 'price_'+ task_id]]

def get_quality(model, task, editors):
    """
    Estimates quality of a task based on task properties and editor's skills
    :param task: pandas Dataframe row, with task info (number_words, language_pair?, domain)
    :param editors: pandas Dataframe, with editors' info (domain's skill, language pairs??)
    :param model: model is a trained model which given the key performance indicators and task specifications predicts
    the output quality for each editor
    :return: pandas Series with quality estimations
    """
    task_id = task['id']
    editors['quality'] = model.predict(editors, task)
    return editors[['id', 'quality_'+ task_id]]

def estimate_best_editor(utility):
    """
    Estimates best single editor by  maximizing utility function considering price and quality
    :param task: pandas Series w/ task properties including price and quality estimation by editor
    # TODO: add constraint for min_quality?
    :return:
    """
    # TODO: utility functio can be more complex, for instance, we can add weights.
    utility['u'] = - utility['price'] + utility['quality']
    best_edit = utility[utility['u'].max()]['id']
    return best_edit

def estimate_best_editors_pipeline(task, max_edits):
    """
    Estimates the best chain of editors to use for a given task, maximizing the price&quality utility function
    :param task: pandas Series w/ task properties including price and quality estimation by editor
    :param max_edits: max no. of editor per task chain
    :return:
    """
    # TODO
    return

def task_db_updater(task):
    """
    task object
    :param task:
    :return:
    """
    global DONE_TASKS_DB
    if (DONE_TASKS_DB[task['ticket_id']] is None):
        DONE_TASKS_DB[task['ticket_id']] = dict()
        DONE_TASKS_DB[task['ticket_id']]['parts'] = tickets.loc[tickets['id'] == task['ticket_id'], 'parts']
    DONE_TASKS_DB[task['ticket_id']][task['sequence_number']] = task

    editor_manager.update_editorsdb(task)

    # If all parts of the ticket sequence were already receive call ticket manager to compile result.
    if all(DONE_TASKS_DB[task['ticket_id']]['parts']) in DONE_TASKS_DB[task['ticket_id']].keys():
        ticket_manager.regroup_tasks(task['ticket_id'])
    return

# read datasets
editors = pd.read_csv("dataset/editors.csv")
editors.rename({"Unnamed: 0": 'No'}, axis='columns', inplace=True)

clients = pd.read_csv("dataset/clients.csv")
clients.rename({"Unnamed: 0": 'No'}, axis='columns', inplace=True)

"""
clients.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 50 entries, 0 to 49
Data columns (total 4 columns):
No          50 non-null int64
id          50 non-null object
domain      50 non-null object
category    50 non-null object
dtypes: int64(1), object(3)
memory usage: 2.0+ KB

clients.category.value_counts()
Small         21
Enterprise    17
Medium        12
Name: category, dtype: int64

clients.domain.value_counts()
travel         24
fintech         9
ecommerce       8
health_care     6
sports          2
gamming         1
Name: domain, dtype: int64

"""


tickets = pd.read_csv("dataset/tickets.csv")
tickets.rename({"Unnamed: 0": 'No', 'client_id': 'client_tid', 'client_id.1':'client_id'}, axis='columns', inplace=True)
tickets_info = pd.merge(tickets, clients, left_on='client_id', right_on='id', suffixes = ('_ticket', '_client'))

tasks = pd.read_csv("dataset/tasks.csv")
tasks.rename({"Unnamed: 0": 'No'}, axis='columns', inplace=True)
# merging tasks and tickets database to have all information in one place
TASKS_INFO = pd.merge(tasks, tickets_info, left_on='ticket_id', right_on='id_ticket', suffixes = ('_task', '_ticket'))
# creating a variable with the total number of tasks in the ticket
TASKS_INFO['parts'] = TASKS_INFO['ticket_id'].map(TASKS_INFO.groupby('ticket_id')['sequence_number'].max())
TASKS_INFO['best_editor'] = ''
TASKS_INFO['content'] = ''

# This is a placeholder for an actual tasks database. A dictionary which keys are the ticket numbers, and each entry
# contains another dict() with the sequence number of each finished task contained in that ticket
DONE_TASKS_DB = dict.fromkeys(tickets['id'].values)


if __name__ == "__main__":
    # Generate some random data for editor's language pairs
    lps = list(tickets['language_pair'].unique())
    synth.synth_lps_data(editors, lps=lps)

    for tckt_id, tckt_tasks in TASKS_INFO.groupby('ticket_id'):

        # make sure the tasks are in the correct order
        tckt_tasks.sort_values(by='sequence_number', ascending=True, inplace=True)
        for idx_task, task in tckt_tasks.iterrows():
            # task = TASKS_INFO.iloc[0,:].copy(deep=True)
            utility = get_prices(task, editors)

            utility = utility.join(get_quality(task, editors))

            task['best_editor'] = estimate_best_editor(utility)
            # If we were to use a chain of editors instead of just one
            # task['best_editors_pipeline'] = estimate_best_editors_pipeline()

            ## Send task to editor using streaming platform
            msg_producer.send_content_service(task)
