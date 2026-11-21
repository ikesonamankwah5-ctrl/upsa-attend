from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from career.models import Opportunity, OpportunitySource


class Command(BaseCommand):

    help = 'Safely restore the original Career Centre opportunities.'

    def handle(self, *args, **options):

        source_count = OpportunitySource.objects.count()
        opportunity_count = Opportunity.objects.count()

        # Already restored: do not import again.
        if source_count == 16 and opportunity_count == 40:
            self.stdout.write(
                self.style.SUCCESS(
                    'Career Centre data already restored. No changes made.'
                )
            )
            return

        # Never overwrite partially populated production tables.
        if source_count != 0 or opportunity_count != 0:
            raise CommandError(
                f'Restoration stopped. Found {source_count} sources '
                f'and {opportunity_count} opportunities. '
                'Manual inspection is required.'
            )

        self.stdout.write('Restoring Career Centre data...')

        call_command('loaddata', 'opportunities_backup.json')

        self.stdout.write(
            self.style.SUCCESS(
                f'Restoration complete. '
                f'Sources: {OpportunitySource.objects.count()}, '
                f'Opportunities: {Opportunity.objects.count()}.'
            )
        )
