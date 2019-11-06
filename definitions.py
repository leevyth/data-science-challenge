from dataclasses import dataclass

domains = ['travel', 'fintech', 'ecommerce', 'sports', 'gamming']
category = [ 'Small' , 'Medium', 'Enterprise']

alpha = 1
beta = 1
Gamma = 1


@dataclass
class Ticket(object):
    id: str
    client_id : str
    tone : str
    topic : str
    number_words : int
    source_language : str
    target_language : str
    quality_score : float
    price : float # sum of all tasks costs

    # def to_hash(self):
    #     return self.__dict__

@dataclass
class Client(object):
    id: str
    domain : str
    category : str

@dataclass
class Task(object):
    id: str
    sequence_number : int
    number_words : int
    ticket_id : str
    cost : float

@dataclass
class Editor(object):
    id: str
    # language_pair : str
    travel_skill : int
    fintech_skill : int
    ecommerce_skill : int
    sport_skill : int
    gamming_skill : int


