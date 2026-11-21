from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import close_old_connections

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util


def fetch_opportunities_job():
    close_old_connections()

    try:
        call_command('fetch_opportunities')
    finally:
        close_old_connections()


class Command(BaseCommand):

    help = 'Start UPSA Attend server and opportunity scheduler together.'

    def handle(self, *args, **options):

        local_timezone = ZoneInfo(settings.TIME_ZONE)

        scheduler = BackgroundScheduler(
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
            name='Fetch opportunities every six hours',
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

        try:
            scheduler.start()

            self.stdout.write(
                self.style.SUCCESS(
                    'UPSA Attend scheduler started.'
                )
            )

            self.stdout.write(
                'Opportunity collection interval: 6 hours.'
            )

            self.stdout.write(
                'Starting Django development server...'
            )

            call_command(
                'runserver',
                use_reloader=False
            )

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING(
                    'Stopping UPSA Attend...'
                )
            )

        finally:
            if scheduler.running:
                scheduler.shutdown(wait=False)

            self.stdout.write(
                self.style.SUCCESS(
                    'UPSA Attend stopped successfully.'
                )
            )