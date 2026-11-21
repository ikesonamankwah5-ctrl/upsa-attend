from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import close_old_connections

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util


def fetch_opportunities_job():
    """Run the opportunity collection command."""

    close_old_connections()

    try:
        call_command('fetch_opportunities')
    finally:
        close_old_connections()


class Command(BaseCommand):

    help = 'Run the UPSA Attend opportunity scheduler.'

    def handle(self, *args, **options):

        local_timezone = ZoneInfo(settings.TIME_ZONE)

        scheduler = BlockingScheduler(
            timezone=local_timezone
        )

        scheduler.add_jobstore(
            DjangoJobStore(),
            'default'
        )

        scheduler.add_job(
            fetch_opportunities_job,
            trigger=IntervalTrigger(
                hours=6,
                timezone=local_timezone
            ),
            id='fetch_opportunities_every_six_hours',
            name='Fetch career opportunities every six hours',
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
            next_run_time=datetime.now(local_timezone),
        )

        scheduler.add_listener(
            util.close_old_connections,
            EVENT_JOB_EXECUTED | EVENT_JOB_ERROR
        )

        self.stdout.write(
            self.style.SUCCESS(
                'UPSA Attend opportunity scheduler is starting.'
            )
        )

        self.stdout.write(
            'Collection frequency: Every 6 hours.'
        )

        self.stdout.write(
            'Timezone: Africa/Accra.'
        )

        try:
            scheduler.start()

        except KeyboardInterrupt:
            scheduler.shutdown()

            self.stdout.write(
                self.style.WARNING(
                    'Opportunity scheduler stopped.'
                )
            )