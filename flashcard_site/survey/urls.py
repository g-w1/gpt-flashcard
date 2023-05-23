from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("get_cards", views.get_cards, name="get_cards"),
   path("submit_card", views.submit_card, name="submit_card"),
   path("review_cards", views.review_cards, name="review_cards"),
]
