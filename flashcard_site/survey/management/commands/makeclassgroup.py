from django.core.management.base import BaseCommand, CommandError
from survey.models import Assessment, SurveyGroup


class Command(BaseCommand):
    help = "Adds a new SurveyGroup and all associated with that"

    def add_arguments(self, parser):
        parser.add_argument(
            "namecode", help="SurveyGroup name (should be a code to enter)", type=str
        )
        parser.add_argument(
            "topics_file", help="file containing the topics_to_make", type=str
        )
        parser.add_argument(
            "cards_file", help="file containing the JSON of the cards", type=str
        )

    def handle(self, *args, **options):
        namecode = options["namecode"]
        topics_to_make = open(options["topics_file"], 'r').read()
        ai_cards = open(options["cards_file"], 'r').read()
        sg = SurveyGroup(
            name=namecode, topics_to_make=topics_to_make, ai_cards=ai_cards
        )
        sg.save()
        self.stdout.write(self.style.SUCCESS(f"Created SurveyGroup {namecode}"))
        questions_start = input(
            "please enter the questions for the initial assessment (json):"
        )
        correct_answers_start = input(
            "please enter the correct answers for the initial assessment (json):"
        )
        questions_end = input(
            "please enter the questions for the final assessment (json):"
        )
        correct_answers_end = input(
            "please enter the correct answers for the final assessment (json):"
        )
        ass = Assessment(
            survey_group=sg,
            questions_start=questions_start,
            correct_answers_start=correct_answers_start,
            questions_end=questions_end,
            correct_answers_end=correct_answers_end,
        )
        ass.save()
        self.stdout.write(self.style.SUCCESS(f"Created Assessment (id: {ass.id})"))
