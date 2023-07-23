from django.core.management.base import BaseCommand, CommandError
from survey.models import Assessment, SurveyGroup
import json


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

        parser.add_argument(
            "beginning_assessment_file",
            help="file containing the JSON of an array of the qs + choices in index 0 and correct answers in index 1",
        )
        parser.add_argument(
            "final_assessment_file",
            help="file containing the JSON of an array of the qs + choices in index 0 and correct answers in index 1",
        )

    def handle(self, *args, **options):
        namecode = options["namecode"]
        topics_to_make = open(options["topics_file"], "r").read()
        ai_cards = open(options["cards_file"], "r").read()
        sg = SurveyGroup(
            name=namecode, topics_to_make=topics_to_make, ai_cards=ai_cards
        )
        sg.save()
        self.stdout.write(self.style.SUCCESS(f"Created SurveyGroup {namecode}"))
        ass_start = json.loads(open(options["beginning_assessment_file"], "r").read())
        ass_end = json.loads(open(options["final_assessment_file"], "r").read())
        questions_start = json.dumps(ass_start[0])
        correct_answers_start = json.dumps(ass_start[1])
        questions_end = json.dumps(ass_end[0])
        correct_answers_end = json.dumps(ass_end[1])
        ass = Assessment(
            survey_group=sg,
            questions_start=questions_start,
            correct_answers_start=correct_answers_start,
            questions_end=questions_end,
            correct_answers_end=correct_answers_end,
        )
        ass.save()
        self.stdout.write(self.style.SUCCESS(f"Created Assessment (id: {ass.id})"))
