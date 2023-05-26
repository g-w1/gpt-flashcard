from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template import loader
import datetime
import json
import math

from .models import (
    Card,
    ReviewStat,
    Assessment,
    AssessmentSubmission,
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
        date_next__lte=datetime.date.today(),
        time_next_today__lte=datetime.datetime.today(),
        queue_type=QUEUE_TYPE_LRN,
    )
    lrn_for_today_card = get_card_from_cards(lrn_for_today)
    if lrn_for_today_card != None:
        return HttpResponse(lrn_for_today_card, content_type="application/json")

    new_failed_for_today = Card.objects.filter(
        date_next__lte=datetime.date.today(),
        time_next_today__lte=datetime.datetime.today(),
        queue_type=QUEUE_TYPE_NEW_FAILED,
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

    # see if there are any cards left today in a few minutes
    later_today = (
        Card.objects.filter(
            date_next=datetime.date.today(),
        )
        .exclude(queue_type=QUEUE_TYPE_NEW)
        .order_by("time_next_today")
    )
    if len(later_today) == 0:
        return HttpResponse(
            json.dumps({"id": None, "laterToday": None}),
            content_type="application/json",
        )
    else:
        amount = len(later_today)
        earliest = math.ceil(
            (
                later_today[0].time_next_today
                - datetime.datetime.now(datetime.timezone.utc)
            ).total_seconds()
            / 60
        )
        return HttpResponse(
            json.dumps(
                {"id": None, "laterToday": {"amount": amount, "earliest_min": earliest}}
            ),
            content_type="application/json",
        )


@login_required
def submit_card(request):
    user = request.user
    # get the card
    if not request.POST:
        return HttpResponse("/submit_card needs a POST request")
    # reset the amount of new cards to 0 if a day (or more) has passed
    if request.user.last_used != datetime.date.today():
        request.user.new_cards_added_today = 0
        request.user.last_used = datetime.date.today()
        request.user.save()
    # do the fancy algo
    req = json.loads(request.POST["body"])
    quality = req["quality"]
    id = req["id"]
    stat_time_for_card = req["time_for_card"]
    card = Card.objects.filter(
        id=id, belongs=user, date_next__lte=datetime.date.today()
    )
    if len(card) != 1:
        return HttpResponse(
            "{'analyzed': false, 'error':'you submitted a card that does not exist, or from another user, or card that is not ready to be displayed yet'}",
            content_type="application/json",
        )
    card = card[0]

    # SETUP THE STATS
    # fill in all the fields that we have now
    stat_belongs = request.user
    stat_card = card
    stat_dtime_now = datetime.datetime.today()
    stat_quality = quality
    stat_interval_before = card.interval
    stat_easiness_before = card.easiness
    stat_date_scheduled_before = card.date_next
    # We can acutally model the cards as some sort of finite state machine, which is really cool!
    # QUALITY:
    # quality = 4: easiness does not change
    # quality = 1: subtract .2
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
        user.save()
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
            card.queue_type = QUEUE_TYPE_NEW_FAILED
            card.interval = 0
            minutes_next = 1
            card.repetitions = 0
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
    if quality == 1:
        card.easiness -= 0.2
        if card.easiness < 1.3:
            card.easiness = 1.3
    elif quality == 4:
        pass  # don't change the easiness
    review_date = datetime.date.today() + datetime.timedelta(card.interval)
    card.date_next = review_date
    if minutes_next != None:
        card.time_next_today = datetime.datetime.today() + datetime.timedelta(
            minutes=minutes_next
        )
    else:
        card.time_next_today = None
    card.save()
    stat_interval_after = card.interval
    stat_easiness_after = card.easiness
    stat_date_scheduled_after = card.date_next
    stat = ReviewStat(
        belongs=stat_belongs,
        card=stat_card,
        dtime_now=stat_dtime_now,
        quality=stat_quality,
        interval_before=stat_interval_before,
        interval_after=stat_interval_after,
        easiness_before=stat_easiness_before,
        easiness_after=stat_easiness_after,
        date_scheduled_before=stat_date_scheduled_before,
        date_scheduled_after=stat_date_scheduled_after,
        time_for_card=stat_time_for_card,
    )
    stat.save()
    return HttpResponse('{"analyzed":true}', content_type="application/json")


@login_required
def submit_assessment_response(request):
    if not request.POST:
        return HttpResponse("/submit_assessment_response needs a POST request")
    user = request.user
    req = json.loads(request.POST["body"])
    assessment = Assessment.objects.filter(
        id=req["assessment_id"], program=user.program
    )
    if len(assessment) != 1:
        return HttpResponse(
            "a user can only submit an assessment in their program OR the id is invalid"
        )
    assessment = assessment[0]
    supplied_answers = req["supplied_answers"]
    # make sure it is valid json
    _ = json.loads(supplied_answers)
    at_beginning = req["at_beginning"]

    a = AssessmentSubmission(
        user_belongs=user,
        assessment_belongs=assessment,
        supplied_answers=supplied_answers,
        at_beginning=req["at_beginning"],
    )
    a.save()
    return HttpResponse('{"analyzed":true}', content_type="application/json")


@login_required
def get_assessment(request):
    # TODO do url param, group is in url
    assert user.group == urlparam_group
