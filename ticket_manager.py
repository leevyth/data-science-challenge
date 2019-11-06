import pandas as pd
import task_manager as task_manager
import copy


def regroup_tasks(ticket_id):
    """
    Concatenates tasks on the task_manager.DONE_TASKS_DB from the correspondent ticket id
    :param ticket_id: str
    :return: str, final revised ticket text
    """
    ticket = copy.deepcopy(task_manager.DONE_TASKS_DB[ticket_id])
    ticket.pop('parts')
    ticket_content = ''
    for task in sorted(ticket.keys()):
        ticket_content = ticket_content.append('\n' + task['content'])

    final_content = revise(ticket_content)

    return final_content

def revise(text):
    """
    Some NLP technique to evaluate and correct the regrouped content for insconsistencies,
    or sending the content to a final editor.
    :param text: concatenated text from ticket
    :return: revised text
    """
    revised_text = text
    return revised_text
