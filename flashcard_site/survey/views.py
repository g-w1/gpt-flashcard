from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import json

from .models import Card

# Create your views here.
def index(request):
	return HttpResponse("At Survey Index TODO")

@login_required
def get_cards(request):
    user = request.user
    reviews_for_today = Card.objects.filter(date_next=datetime.date.today())
    if len(reviews_for_today) > 0:
        review = reviews_for_today[0]
        id = review.id
        front = review.front
        back = review.back
        return HttpResponse(json.dumps({'id': id, 'front': front, 'back': back}), content_type='application/json')
@login_required
def submit_card(request):
    if not request.POST:
        return HttpResponse('/submit_card needs a POST request')
    req = json.parse(request.POST['body'])
    ease = req['ease']
    id = req['id']
    card = Card.objects.filter(id=req['id'], user=request.user)
    if len(card) != 1:
        return HttpResponse("stop trying to hack")
    card = card[0]
    # TODO business logic
    return HttpResponse(f'analyzed {card}')
