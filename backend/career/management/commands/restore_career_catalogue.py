from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from career.models import (
    AcademicProgramme,
    Career,
    CareerAcademicProgramme,
    CareerSkill,
    CareerQuestion,
    CareerAnswerOption,
    CareerAnswerWeight,
)


class Command(BaseCommand):

    help = 'Safely restore Career Catalogue and Career Quest data.'

    EXPECTED_COUNTS = {
        AcademicProgramme: 22,
        Career: 41,
        CareerAcademicProgramme: 223,
        CareerSkill: 208,
        CareerQuestion: 15,
        CareerAnswerOption: 63,
        CareerAnswerWeight: 264,
    }

    def handle(self, *args, **options):

        current_counts = {
            model: model.objects.count()
            for model in self.EXPECTED_COUNTS
        }

        if current_counts == self.EXPECTED_COUNTS:
            self.stdout.write(
                self.style.SUCCESS(
                    'Career data already restored. No changes made.'
                )
            )
            return

        if any(current_counts.values()):
            details = '\n'.join(
                f'{model.__name__}: {count}'
                for model, count in current_counts.items()
            )

            raise CommandError(
                'Restoration stopped. Some tables already contain data:\n'
                + details
            )

        self.stdout.write('Starting Career Catalogue restoration...')

        with transaction.atomic():
            call_command(
                'loaddata',
                'career_catalogue_backup.json',
            )

            restored_counts = {
                model: model.objects.count()
                for model in self.EXPECTED_COUNTS
            }

            if restored_counts != self.EXPECTED_COUNTS:
                raise CommandError(
                    'Restoration verification failed. '
                    'The transaction has been rolled back.'
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Career Catalogue and Career Quest restored successfully!'
            )
        )

        for model, count in restored_counts.items():
            self.stdout.write(f'{model.__name__}: {count}')