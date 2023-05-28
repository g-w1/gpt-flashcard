from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_cards", views.get_cards, name="get_cards"),
    path("submit_card", views.submit_card, name="submit_card"),
    path("review_cards", views.review_cards, name="review_cards"),
    path(
        "submit_assessment_response",
        views.submit_assessment_response,
        name="submit_assessment_response",
    ),
    path("add_time", views.add_time, name="add_time"),
    path("get_assessment/<str:subject_group>/<str:start>", views.get_assessment, name="get_assessment"), # we just convert it to a bool
    path('initial_survey', views.initial_survey_view, name='initial_survey'),
]
