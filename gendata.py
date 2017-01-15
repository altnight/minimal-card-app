import random
import json

from faker import Factory

f = Factory.create()


class DebuggingBase(object):
    def __repr__(self):
        return f'{self.__class__.__name__}<id::{self.id}>'

    @property
    def name(self):
        return self.__repr__()


class Board(DebuggingBase):
    _id_sequence = 0

    def __init__(self):
        self.id = self.board_sequence()
        self.lists = []

    @classmethod
    def board_sequence(cls):
        cls._id_sequence += 1
        return cls._id_sequence

    def add_list(self, list):
        self.lists.append(list)

    def add_lists(self, lists):
        for list in lists:
            self.add_list(list)

    def to_data(self):
        lists = []
        for i, _list in enumerate(self.lists):
            d = _list.to_data()
            d["index"] = i
            lists.append(d)

        return {
            "id": self.id,
            "name": self.name,
            "lists": lists,
        }


class List(DebuggingBase):
    _id_sequence = 0

    def __init__(self, board):
        self.id = self.list_sequence()
        self.board = board
        self.cards = []

    @classmethod
    def list_sequence(cls):
        cls._id_sequence += 1
        return cls._id_sequence

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.add_card(card)

    def to_data(self):
        cards = []
        for i, _list in enumerate(self.cards):
            d = _list.to_data()
            d["index"] = i
            cards.append(d)
        return {
            "id": self.id,
            "name": self.name,
            "cards": cards,
        }


class Card(DebuggingBase):
    _id_sequence = 0

    def __init__(self, list):
        self.id = self.card_sequence()
        self.list = list
        self.comments = []
        self.description = f.text()
        self.checklists = []

    @classmethod
    def card_sequence(cls):
        cls._id_sequence += 1
        return cls._id_sequence

    def add_comment(self, comment):
        self.comments.append(comment)

    def add_comments(self, comments):
        for comment in comments:
            self.add_comment(comment)

    def add_checklist(self, checklist):
        self.checklists.append(checklist)

    def add_checklists(self, checklists):
        for checklist in checklists:
            self.add_checklists(checklist)

    def to_data(self):
        checklists = []
        for i, _checklist in enumerate(self.checklists):
            d = _checklist.to_data()
            d["index"] = i
            checklists.append(d)
        return {
            "id": self.id,
            "list_id": self.list.id,
            "name": f"{self.name}::{f.name()}",
            "description": self.description,
            "comments": [comment.to_data() for comment in self.comments],
            "checklists": checklists,
        }


class Comment(DebuggingBase):
    _id_sequence = 0

    def __init__(self, card):
        self.id = self.comment_sequence()
        self.card = card

    @classmethod
    def comment_sequence(cls):
        cls._id_sequence += 1
        return cls._id_sequence

    def to_data(self):
        return {
            "id": self.id,
            "body": f"{self.name}: {f.text()}",
        }


class Checklist(DebuggingBase):
    _id_sequence = 0

    def __init__(self, card):
        self.id = self.checklist_sequence()
        self.card = card
        self.checklist_items = []

    @classmethod
    def checklist_sequence(cls):
        cls._id_sequence += 1
        return cls._id_sequence

    def add_checklist_item(self, checklist_item):
        self.checklist_items.append(checklist_item)

    def add_checklist_items(self, checklist_items):
        for checklist_item in checklist_items:
            self.add_checklist_items(checklist_item)

    def to_data(self):
        checklist_items = []
        for i, _checklist_item in enumerate(self.checklist_items):
            d = _checklist_item.to_data()
            d["index"] = i
            checklist_items.append(d)

        return {
            "id": self.id,
            "name": f"{self.name}: {f.text()[:10]}",
            "checklist_items": checklist_items,
        }


class ChecklistItem(DebuggingBase):
    _id_sequence = 0

    def __init__(self, checklist):
        self.id = self.checklistitem_sequence()
        self.checklist = checklist
        self.is_done = random.choice([True, False])

    @classmethod
    def checklistitem_sequence(cls):
        cls._id_sequence += 1
        return cls._id_sequence

    def to_data(self):
        return {
            "id": self.id,
            "is_done": self.is_done,
            "body": f"{self.name}: {f.text()[:20]}",
        }


BOARD_RANGE = 3
CARD_RANGE = 8
COMMENT_RANGE = 10
LIST_RANGE = 3
CHECKLIST_RANGE = 10
CHECKLIST_ITEM_RANGE = 30


def gen():
    board = Board()
    lists = [List(board)
             for i in range(LIST_RANGE)]
    cards = [Card(lists[random.randint(0, LIST_RANGE - 1)])
             for i in range(CARD_RANGE)]
    comments = [Comment(cards[random.randint(0, CARD_RANGE - 1)])
                for i in range(COMMENT_RANGE)]
    checklists = [Checklist(cards[random.randint(0, CARD_RANGE - 1)])
                  for i in range(CHECKLIST_RANGE)]
    checklist_items = [ChecklistItem(checklists[random.randint(0, CHECKLIST_RANGE - 1)])
                       for i in range(CHECKLIST_ITEM_RANGE)]

    for card in cards:
        for list in lists:
            if card.list == list:
                list.add_card(card)

    for comment in comments:
        for card in cards:
            if comment.card == card:
                card.add_comment(comment)

    for checklist in checklists:
        for card in cards:
            if checklist.card == card:
                card.add_checklist(checklist)

    for checklist_item in checklist_items:
        for checklist in checklists:
            if checklist_item.checklist == checklist:
                checklist.add_checklist_item(checklist_item)

    board.add_lists(lists)
    return board.to_data()


results = [gen() for i in range(BOARD_RANGE)]
ret = json.dumps({'results': results,
                  'seq': {'board': Board._id_sequence,
                          'list': List._id_sequence,
                          'comment': Comment._id_sequence,
                          'card': Card._id_sequence,
                          'checklist': Checklist._id_sequence,
                          'checklist_item': ChecklistItem._id_sequence}
                  }, indent=2)

output = f'''
export default {ret}
'''
print(output)
