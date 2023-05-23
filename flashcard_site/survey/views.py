from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
import json

from .models import (
    Card,
    CARD_TYPE_NEW,
    CARD_TYPE_LRN,
    CARD_TYPE_REV,
    CARD_TYPE_RLN,
    QUEUE_TYPE_NEW,
    QUEUE_TYPE_LRN,
    QUEUE_TYPE_REV,
    NEW_ADDED_EVERY_DAY,
)


def index(request):
    return HttpResponse("At Survey Index TODO")


def get_card_from_cards(cards):
    if len(cards) > 0:
        review = cards[0]
        id = review.id
        front = review.front
        back = review.back
        card_type = review.card_type
        queue_type = review.queue_type
        return json.dumps(
            {
                "id": id,
                "front": front,
                "back": back,
                "card_type": card_type,
                "queue_type": queue_type,
            }
        )
    else:
        return None


@login_required
def get_cards(request):
    user = request.user

    lrn_for_today = Card.objects.filter(
        date_next__lte=datetime.date.today(), queue_type=QUEUE_TYPE_LRN
    )
    lrn_for_today_card = get_card_from_cards(lrn_for_today)
    if lrn_for_today_card != None:
        return HttpResponse(lrn_for_today_card, content_type="application/json")

    rev_for_today = Card.objects.filter(
        date_next__lte=datetime.date.today(), queue_type=QUEUE_TYPE_REV
    )
    rev_for_today_card = get_card_from_cards(lrn_for_today)
    if rev_for_today_card != None:
        return HttpResponse(rev_for_today_card, content_type="application/json")

    if user.new_cards_added_today > 5:
        rev_for_today = Card.objects.filter(
            date_next__lte=datetime.date.today(), queue_type=QUEUE_TYPE_NEW
        )
        rev_for_today_card = get_card_from_cards(lrn_for_today)
        if rev_for_today_card != None:
            return HttpResponse(rev_for_today_card, content_type="application/json")
    return HttpResponse(json.dumps({"id": None}), content_type="application/json")


@login_required
def submit_card(request):
    if not request.POST:
        return HttpResponse("/submit_card needs a POST request")
    req = json.parse(request.POST["body"])
    quality = req["quality"]
    id = req["id"]
    card = Card.objects.filter(id=req["id"], user=request.user)
    if len(card) != 1:
        return HttpResponse("stop trying to hack")
    card = card[0]
    if quality < 3:
        card.interval = 0  # do it again today
        card.repititions = 0  # reset the streak
    else:
        if card.repititions == 0:
            card.interval = 1
        elif card.repititions == 1:
            card.interval == 6  # TODO is 6 correct?
        else:
            card.interval = ceil(card.interval * card.easinessA)

        card.repititions += 1
    card.easiness += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    if card.easiness < 1.3:
        card.easiness = 1.3
    review_date = datetime.date.today() + datetime.timedelta(interval)
    # TODO graduate card and decrement user.new_cards_added_today
    return HttpResponse(f"analyzed {card}")
