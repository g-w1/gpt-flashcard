from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_cards", views.get_cards, name="get_cards"),
    path("submit_card", views.submit_card, name="submit_card"),
    path("review_cards", views.review_cards, name="review_cards"),
    path(
        "get_assessment/<str:start>",
        views.get_assessment,
        name="get_assessment",
    ),  # we just convert it to a bool
    path("initial_survey", views.initial_survey_view, name="initial_survey"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_card", views.add_card, name="add_card"),
]
