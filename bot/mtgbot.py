import re
from queue import Queue
import json
from mtgsdk import Card
from fbchat import Client
from fbchat.models import *


def parse_message(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
    if author_id == self.uid:
        return

    text = message_object.text.lower()

    match = re.search(fetch, text)

    if match:
        cards = Card.where(name=match.group(1)).all()
        for i in range(len(cards)):
            print(cards[i].name)
        cards = removeDuplicates(cards)
        if len(cards) > 1:
            cardlist = ""
            for i in range(len(cards)):
                cardlist += cards[i].name + "\n"

            whichone = "There are " + str(len(cards)) + " cards with that name. " + \
                                                        "Please a specific one from the following:\n" + cardlist
            client.send(Message(text=whichone), thread_id=thread_id, thread_type=thread_type)
        else:
            sendcard(cards[0], thread_id, thread_type)
    elif re.search(begone, text):
        self.listening = False
        return


def sendcard(card, thread_id, thread_type):
    info = "Name: " + card.name + "\n"
    if(card.mana_cost != None):
        info += "Mana Cost: " + card.mana_cost + "\n"
    info += "Type: "
    if(card.supertypes != None):
        info += "".join(list(card.supertypes)) + " "
    info += "".join(list(card.types))
    if(card.subtypes != None):
        info += " - " + "".join(list(card.subtypes))
    info += "\n"
    info += "Rarity: " + card.rarity + "\n"
    info += "Text: " + card.text + "\n"
    if(card.power != None and card.toughness != None):
        info += "Power/Toughness: " + str(card.power) + " / " + str(card.toughness) + "\n"
    if(card.loyalty != None):
        info += "Loyalty: " + str(card.loyalty) + "\n"
    client.send(Message(text=info), thread_id=thread_id, thread_type=thread_type)


def removeDuplicates(cards):
    i = 0
    while(i < len(cards)):
        j = i + 1
        while(j < len(cards)):
            #print(i, cards[i].name, j, cards[j].name)
            if(cards[j].name == cards[i].name):
                cards.pop(j).name
            else:
                j += 1
        i += 1
    return cards


class MTG(Client):
    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        self.markAsDelivered(author_id, thread_id)
        parse_message(self, mid, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg)

    def onFriendRequest(self, from_id=None, msg=None):
        print("Got friend request from " + str(from_id))
        self.friendConnect(from_id)


if __name__ == '__main__':
    with open("conf.json", "r") as f:
        config = json.load(f)

    client = MTG(config["facebook"]["email"], config["facebook"]["password"])

    fetch = re.compile("{{([\w\s]*.*)}}")
    begone = re.compile("(BEGONE JACE)")
    requests = Queue()

    client.listen()
    #client.send(Message(text='Hi me!'), thread_id=client.uid, thread_type=ThreadType.USER)
    client.logout()
