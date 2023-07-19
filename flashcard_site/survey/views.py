from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .forms import InitialSurveyForm, CustomUserCreationForm, LoginForm, CardForm
import datetime
from django.utils import timezone
import json
import math
import random

from functools import wraps

from .models import (
    Card,
    User,
    ReviewStat,
    Assessment,
    AssessmentSubmission,
    InitialSurvey,
    SurveyGroup,
    QUEUE_TYPE_NEW,
    QUEUE_TYPE_NEW_FAILED,
    QUEUE_TYPE_LRN,
    QUEUE_TYPE_REV,
    NEW_ADDED_EVERY_DAY,
    EXPERIMENT_GROUP_WRITING,
    EXPERIMENT_GROUP_AI,
)


def check_surveys_completed(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.needs_to_take_survey:
                group = "writing" if request.user.survey_group == 1 else "LLM"
                message = (
                    "write and study your own flashcards"
                    if request.user.survey_group == 1
                    else "study the flashcards written by a large language model (LLM)"
                )
                messages.info(
                    request,
                    f"You need to complete the survey before doing anything else.\nYou are in the {group} group, which means you {message}",
                )
                return redirect("initial_survey")
            elif request.user.needs_to_take_initial_assessment:
                messages.info(
                    request,
                    "You need to complete the initial assessment before doing anything else",
                )
                return redirect("/get_assessment/true")
            elif request.user.needs_to_take_final_assessment:
                messages.info(
                    request,
                    "You need to complete the final assessment before doing anything else",
                )
                return redirect("/get_assessment/false")
            else:
                return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view


def error(message):
    s = f'{{"analyzed": false, "error":"{message}"}}'
    return HttpResponse(
        s,
        content_type="application/json",
    )


@check_surveys_completed
def index(request):
    return render(request, "survey/index.html")


def about(request):
    return render(request, "survey/about.html")


@login_required
@check_surveys_completed
def review_cards(request):
    return render(request, "survey/review_cards.html", {})


def get_card_from_cards(cards, num_cards_to_do_today):
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
                "numToDoToday": num_cards_to_do_today,
            }
        )
    else:
        return None


@login_required
def get_cards(request):
    user = request.user
    num_cards_to_do_today = user.num_cards_to_do_today
    cards_for_user = Card.objects.filter(belongs=user, suspended=False)
    # these are the ones that use time_next_today, because they are sensitive to minutes
    lrn_for_today = cards_for_user.filter(
        Q(date_next__lte=timezone.localdate())
        & (
            Q(time_next_today__lte=timezone.localtime())
            | Q(time_next_today__isnull=True)
        )
        & Q(queue_type=QUEUE_TYPE_LRN)
    )
    lrn_for_today_card = get_card_from_cards(lrn_for_today, num_cards_to_do_today)
    if lrn_for_today_card != None:
        return HttpResponse(lrn_for_today_card, content_type="application/json")

    new_failed_for_today = cards_for_user.filter(
        date_next__lte=timezone.localdate(),
        time_next_today__lte=timezone.localtime(),
        queue_type=QUEUE_TYPE_NEW_FAILED,
    )
    new_failed_for_today_card = get_card_from_cards(
        new_failed_for_today, num_cards_to_do_today
    )
    if new_failed_for_today_card != None:
        return HttpResponse(new_failed_for_today_card, content_type="application/json")

    rev_for_today = cards_for_user.filter(
        date_next__lte=timezone.localdate(), queue_type=QUEUE_TYPE_REV
    )
    rev_for_today_card = get_card_from_cards(rev_for_today, num_cards_to_do_today)
    if rev_for_today_card != None:
        return HttpResponse(rev_for_today_card, content_type="application/json")

    if user.new_cards_added_today < NEW_ADDED_EVERY_DAY:
        new_for_today = cards_for_user.filter(
            date_next__lte=timezone.localdate(), queue_type=QUEUE_TYPE_NEW
        )
        new_for_today_card = get_card_from_cards(new_for_today, num_cards_to_do_today)
        if new_for_today_card != None:
            return HttpResponse(new_for_today_card, content_type="application/json")

    # see if there are any cards left today in a few minutes
    later_today = (
        cards_for_user.filter(
            date_next=timezone.localdate(), time_next_today__isnull=False
        )
        .exclude(queue_type=QUEUE_TYPE_NEW)
        .order_by("time_next_today")
    )
    if len(later_today) == 0:
        num_new_for_today = (
            cards_for_user.filter(
                date_next__lte=timezone.localdate(), queue_type=QUEUE_TYPE_NEW
            )
        ).count()
        if num_new_for_today == 0:
            return HttpResponse(
                json.dumps(
                    {
                        "id": None,
                        "laterToday": None,
                        "numToDoToday": num_cards_to_do_today,
                    }
                ),
                content_type="application/json",
            )
        else:
            return HttpResponse(
                json.dumps(
                    {
                        "id": None,
                        "laterToday": None,
                        "newAvail": True,
                        "numToDoToday": num_cards_to_do_today,
                    }
                ),
                content_type="application/json",
            )

    else:
        amount = len(later_today)
        earliest = math.ceil(
            (later_today[0].time_next_today - timezone.localtime()).total_seconds() / 60
        )
        return HttpResponse(
            json.dumps(
                {
                    "id": None,
                    "laterToday": {
                        "amount": amount,
                        "earliest_min": earliest,
                    },
                    "numToDoToday": num_cards_to_do_today,
                }
            ),
            content_type="application/json",
        )


@login_required
def submit_card(request):
    user = request.user
    # get the card
    if not request.POST:
        return error("/submit_card needs a POST request")
    # reset the amount of new cards to 0 if a day (or more) has passed
    if request.user.last_used != timezone.localdate():
        request.user.new_cards_added_today = 0
        request.user.last_used = timezone.localdate()
        request.user.save()
    # do the fancy algo
    req = json.loads(request.POST["body"])
    quality = req["quality"]
    id = req["id"]
    stat_time_for_card = req["time_for_card"]
    card = Card.objects.filter(id=id, belongs=user, date_next__lte=timezone.localdate())
    if len(card) != 1:
        return error(
            "you submitted a card that does not exist, or from another user, or card that is not ready to be displayed yet",
        )
    card = card[0]
    suspend = req["suspend"]
    if suspend:
        card.suspended = True
        card.save()
        return HttpResponse('{"analyzed":true}', content_type="application/json")

    # SETUP THE STATS
    # fill in all the fields that we have now
    stat_belongs = request.user
    stat_card = card
    stat_dtime_now = timezone.localtime()
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
            minutes_next = 3
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
    review_date = timezone.localdate() + datetime.timedelta(card.interval)
    card.date_next = review_date
    if minutes_next != None:
        card.time_next_today = timezone.localtime() + datetime.timedelta(
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


# Sees if it is 'true'
def b(boo):
    return boo == "true" or boo == "True"


@login_required
def get_assessment(request, start):
    start = b(start)
    user = request.user

    ass = Assessment.objects.get(survey_group=user.survey_group)

    # Check if the user has already submitted an assessment for this subject group
    if AssessmentSubmission.objects.filter(
        user_belongs=user, assessment_belongs=ass, at_beginning=start
    ).exists():
        return redirect("index")

    if not start:
        if not user.final_assessment_is_due():
            return redirect("index")

    if start:
        questions = ass.questions_start
        correct_answers = json.loads(ass.correct_answers_start)
    else:
        questions = ass.questions_end
        correct_answers = json.loads(ass.correct_answers_end)

    if not request.POST:
        return render(request, "survey/assess.html", {"questions": questions})
    else:
        # we are submitting it
        req = json.loads(request.POST["body"])
        answers = req["answers"]
        time = req["time"]

        if len(answers) != len(correct_answers):
            return error("The length of the answers is not correct.")

        sub = AssessmentSubmission(
            user_belongs=user,
            assessment_belongs=ass,
            supplied_answers=json.dumps(answers),
            at_beginning=start,
            time_taken=time,  # Store the time taken in the AssessmentSubmission object
        )
        sub.save()

        return redirect("index")


def initial_survey_view(request):
    if InitialSurvey.objects.filter(user=request.user).exists():
        return redirect("index")
    if request.method == "POST":
        form = InitialSurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.user = request.user
            survey.time_taken = int(float(request.POST["time_taken"]))
            survey.save()
            ## TODO redirect to onboarding page
            return redirect("index")

    else:
        form = InitialSurveyForm()

    return render(request, "survey/initial_survey.html", {"form": form})


def get_disto_experiment_groups_in_survey_group(survey_group):
    users = User.objects.filter(survey_group=survey_group)
    writing = 0
    ai = 0
    for user in users:
        if user.experiment_group == EXPERIMENT_GROUP_WRITING:
            writing += 1
        elif user.experiment_group == EXPERIMENT_GROUP_AI:
            ai += 1
        else:
            assert False  # the experiment group should be one of the three
    return [writing, ai]


def get_experiment_group_for_next_user(survey_group):
    distros = get_disto_experiment_groups_in_survey_group(survey_group)
    # Check if all groups have the same distribution
    if distros[0] == distros[1]:
        # if yes, return a random group
        return random.choice([EXPERIMENT_GROUP_WRITING, EXPERIMENT_GROUP_AI])
    else:
        # if no, return the group with the least distribution
        if distros[0] == min(distros):
            return EXPERIMENT_GROUP_WRITING
        else:
            return EXPERIMENT_GROUP_AI


### USER STUFF
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.experiment_group = get_experiment_group_for_next_user(
                user.survey_group
            )
            user.time_for_writing = (
                None if user.experiment_group != EXPERIMENT_GROUP_WRITING else 0
            )
            user.date_final_opens = timezone.localdate() + datetime.timedelta(
                7 * 4
            )  # TODO make it not 4 weeks
            user.save()
            email = form.cleaned_data["email"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(email=email, password=raw_password)
            if user.experiment_group == EXPERIMENT_GROUP_AI:
                user.add_ai_cards_from_survey_group()
            login(request, user)
            user.send_registration_email()  # TODO maybe queue this for less latency? or just spawn it in a thread
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "survey/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"], password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = LoginForm()
    return render(request, "survey/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
@check_surveys_completed
def add_card(request):
    if request.user.experiment_group == EXPERIMENT_GROUP_WRITING:
        if request.user.time_for_writing == None:
            request.user.time_for_writing = 0

        if request.method == "POST":
            time_to_create = int(float(request.POST["timeToCreate"]))
            form = CardForm(request.POST)
            if form.is_valid():
                card = form.save(commit=False)
                card.belongs = request.user
                card.save()
                request.user.time_for_writing += time_to_create
                request.user.save()
                return redirect("add_card")
        else:
            form = CardForm()

        return render(
            request,
            "survey/add_card.html",
            {"form": form, "topics": request.user.topics_to_make},
        )
    else:
        return redirect("index")
