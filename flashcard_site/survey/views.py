from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template import loader
import datetime
import json
import math

from .models import (
    Card,
    QUEUE_TYPE_NEW,
    QUEUE_TYPE_NEW_FAILED,
    QUEUE_TYPE_LRN,
    QUEUE_TYPE_REV,
    NEW_ADDED_EVERY_DAY,
)


def index(request):
    return HttpResponse("At Survey Index TODO")


@login_required
def review_cards(request):
    return HttpResponse(
        loader.get_template("survey/review_cards.html").render({}, request)
    )


def get_card_from_cards(cards):
    if len(cards) > 0:
        review = cards[0]
        id = review.id
        front = review.front
        back = review.back
        queue_type = review.queue_type
        return json.dumps(
            {
                "id": id,
                "front": front,
                "back": back,
                "queue_type": queue_type,
            }
        )
    else:
        return None


@login_required
def get_cards(request):
    user = request.user
    # these are the ones that use time_next_today, because they are sensitive to minutes
    lrn_for_today = Card.objects.filter(
        date_next__lte=datetime.date.today(), time_next_today__lte=datetime.datetime.today(), queue_type=QUEUE_TYPE_LRN
    )
    lrn_for_today_card = get_card_from_cards(lrn_for_today)
    if lrn_for_today_card != None:
        return HttpResponse(lrn_for_today_card, content_type="application/json")

    new_failed_for_today = Card.objects.filter(
        date_next__lte=datetime.date.today(), time_next_today__lte=datetime.datetime.today(), queue_type=QUEUE_TYPE_NEW_FAILED
    )
    new_failed_for_today_card = get_card_from_cards(new_failed_for_today)
    if new_failed_for_today_card != None:
        return HttpResponse(new_failed_for_today_card, content_type="application/json")

    rev_for_today = Card.objects.filter(
        date_next__lte=datetime.date.today(), queue_type=QUEUE_TYPE_REV
    )
    rev_for_today_card = get_card_from_cards(rev_for_today)
    if rev_for_today_card != None:
        return HttpResponse(rev_for_today_card, content_type="application/json")

    if user.new_cards_added_today < NEW_ADDED_EVERY_DAY:
        new_for_today = Card.objects.filter(
            date_next__lte=datetime.date.today(), queue_type=QUEUE_TYPE_NEW
        )
        new_for_today_card = get_card_from_cards(new_for_today)
        if new_for_today_card != None:
            return HttpResponse(new_for_today_card, content_type="application/json")
    return HttpResponse(json.dumps({"id": None}), content_type="application/json")


@login_required
def submit_card(request):
    user = request.user
    # get the card
    if not request.POST:
        return HttpResponse("/submit_card needs a POST request")
    print(request.POST)
    req = json.loads(request.POST["body"])
    quality = req["quality"]
    id = req["id"]
    card = Card.objects.filter(
        id=id, belongs=user, date_next__lte=datetime.date.today()
    )
    if len(card) != 1:
        return HttpResponse(
            "{'analyzed': false, 'error':'you submitted a card that does not exist, or from another user, or card that is not ready to be displayed yet'}",
            content_type="application/json",
        )
    card = card[0]

    # QUALITY:
    # quality = 5: add .1 to easiness
    # quality = 4: easiness does not change
    # quality = 3: subtract .14
    # quality = 2: subtract .32
    # quality = 1: subtract .54
    minutes_next = None
    if card.queue_type == QUEUE_TYPE_NEW:
        if quality > 3:
            card.queue_type = QUEUE_TYPE_LRN
            card.interval = 0
            minutes_next = 5
            card.repetitions = 1
        else:
            card.queue_type = QUEUE_TYPE_NEW_FAILED
            card.interval = 0
            minutes_next = 1
            card.repetitions = 0
        user.new_cards_added_today += 1
    # the same as previous, but we don't increment the new card max counter
    elif card.queue_type == QUEUE_TYPE_NEW_FAILED:
        if quality > 3:
            card.queue_type = QUEUE_TYPE_LRN
            card.interval = 0
            minutes_next = 5
            card.repetitions = 1
        else:
            card.queue_type = QUEUE_TYPE_NEW_FAILED
            card.interval = 0
            minutes_next = 1
            card.repetitions = 0
    elif card.queue_type == QUEUE_TYPE_LRN:
        if quality > 3:
            card.queue_type = QUEUE_TYPE_REV
            card.interval = 1
            card.repetitions = 1
        else:
            card.queue_type = QUEUE_TYPE_LRN
            card.interval = 0
            minutes_next = 1
            card.repitin = 0
    elif card.queue_type == QUEUE_TYPE_REV:
        if quality < 3:
            card.interval = 0  # do it again today
            minutes_next = 5
            card.repetitions = 0  # reset the streak
            card.queue_type = QUEUE_TYPE_LRN
        else:
            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval == 3
            else:
                card.interval = math.ceil(card.interval * card.easiness)
            card.repetitions += 1
    else:
        assert False  # we encountered a wrong queue_type
    card.easiness += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    if card.easiness < 1.3:
        card.easiness = 1.3
    review_date = datetime.date.today() + datetime.timedelta(card.interval)
    card.date_next = review_date
    if minutes_next != None:
        card.time_next_today = datetime.datetime.today() + datetime.timedelta(minutes=minutes_next)
    else:
        card.time_next_today = None
    card.save()
    user.save()
    return HttpResponse('{"analyzed":true}', content_type="application/json")
