import pandas as pd


EDITORS = pd.read_csv("dataset/editors.csv")
EDITORS.rename({"Unnamed: 0": 'No'}, axis='columns', inplace=True)


def update_editorsdb(task):
    """
    updates editors' database with rating of the performed task
    :param task: pandas Dataframe row, with task info. The task should now have a new field 'editors_rating'
    """
    global EDITORS
    editor_id = task['best_editor']
    domain = task['domain']
    lp = task['language_pair']
    editor_row = EDITORS[(EDITORS['id'] == editor_id) & (EDITORS['language_pair'] == lp)]
    # calculates new domain quality as a mean of previous translations and the new one
    editor_row[domain] = (editor_row[domain] * editor_row['no_tasks_' + domain] + task['editors_rating']) / \
                         (editor_row['no_tasks_' + domain] + 1 )
    editor_row['no_tasks_' + domain] = editor_row['no_tasks_' + domain] + 1
    editor_row['total_tasks'] = editor_row['total_tasks'] + 1
    # Update last task info suggested for editor's db. New selection done, for all duplicated editor id entries, in
    # case there is one per language pair
    EDITORS.loc[EDITORS['id'] == editor_id, 'last_task_datetime'] = pd.datetime.now()
    return