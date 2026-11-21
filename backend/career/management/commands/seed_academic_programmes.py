from django.core.management.base import BaseCommand
from django.utils.text import slugify

from career.models import AcademicProgramme


class Command(BaseCommand):

    help = 'Seed official UPSA Diploma and Undergraduate programmes.'

    PROGRAMMES = [

        # =================================================
        # UNDERGRADUATE PROGRAMMES
        # =================================================

        {
            'name': 'Bachelor of Science in Agribusiness and Finance',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Arts in Applied French and Communications',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Data Science and Analytics',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Applied Statistics',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Laws (LLB)',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Arts in Communication Studies',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Logistics and Transport Management',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Arts in Public Relations Management',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Accounting',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Accounting and Finance',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Business Economics',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Actuarial Science',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Banking and Finance',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Business Administration',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Information Technology',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Applied Marketing',
            'type': 'UNDERGRADUATE',
        },
        {
            'name': 'Bachelor of Science in Real Estate Management and Finance',
            'type': 'UNDERGRADUATE',
        },

        # =================================================
        # DIPLOMA PROGRAMMES
        # =================================================

        {
            'name': 'Diploma in Accounting',
            'type': 'DIPLOMA',
        },
        {
            'name': 'Diploma in Marketing',
            'type': 'DIPLOMA',
        },
        {
            'name': 'Diploma in Management',
            'type': 'DIPLOMA',
        },
        {
            'name': 'Diploma in Public Relations',
            'type': 'DIPLOMA',
        },
        {
            'name': 'Diploma in Information Technology Management',
            'type': 'DIPLOMA',
        },
    ]

    def handle(self, *args, **options):

        created_count = 0
        updated_count = 0

        for item in self.PROGRAMMES:

            programme, created = AcademicProgramme.objects.update_or_create(
                name=item['name'],
                defaults={
                    'slug': slugify(item['name']),
                    'programme_type': item['type'],
                    'is_active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created: {programme.name}'
                    )
                )
            else:
                updated_count += 1

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Seeding completed. Created: {created_count}, '
                f'Already existing/updated: {updated_count}.'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Total academic programmes: '
                f'{AcademicProgramme.objects.count()}'
            )
        )