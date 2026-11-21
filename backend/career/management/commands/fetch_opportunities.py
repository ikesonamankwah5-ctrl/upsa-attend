import calendar
from datetime import datetime, timezone as dt_timezone
from urllib.error import URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

import feedparser

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone
from django.utils.html import strip_tags

from career.models import Opportunity, OpportunitySource


def detect_category(title, description):
    text = f'{title} {description}'.lower()

    keywords = {
        Opportunity.INTERNSHIP: [
            'internship', 'intern', 'industrial attachment'
        ],
        Opportunity.SCHOLARSHIP: [
            'scholarship', 'study abroad', 'tuition'
        ],
        Opportunity.GRANT: [
            'grant', 'funding', 'entrepreneurship'
        ],
        Opportunity.COMPETITION: [
            'competition', 'challenge', 'contest'
        ],
        Opportunity.FELLOWSHIP: [
            'fellowship', 'fellow'
        ],
        Opportunity.VOLUNTEERING: [
            'volunteer', 'volunteering'
        ],
        Opportunity.SKILLS: [
            'certification', 'training', 'bootcamp', 'workshop'
        ],
        Opportunity.EVENT: [
            'conference', 'summit', 'career fair', 'webinar'
        ],
        Opportunity.JOB: [
            'job vacancy', 'graduate trainee', 'employment'
        ],
    }

    for category, terms in keywords.items():
        if any(term in text for term in terms):
            return category

    return Opportunity.OTHER


def fetch_feed(feed_url):
    """
    Download an RSS feed with a timeout and identify
    unavailable or excessively large feeds.
    """

    request = Request(
        feed_url,
        headers={
            'User-Agent': 'UPSA-Attend Opportunity Collector/1.0'
        }
    )

    with urlopen(request, timeout=25) as response:
        content = response.read(5 * 1024 * 1024 + 1)

    if len(content) > 5 * 1024 * 1024:
        raise ValueError('RSS feed exceeds the 5 MB size limit.')

    return feedparser.parse(content)


def get_published_date(entry):
    """
    Convert an RSS publication date into a Python date.
    """

    published_parsed = (
        entry.get('published_parsed')
        or entry.get('updated_parsed')
    )

    if not published_parsed:
        return None

    timestamp = calendar.timegm(published_parsed)

    published_at = datetime.fromtimestamp(
        timestamp,
        tz=dt_timezone.utc
    )

    return published_at.date()


class Command(BaseCommand):

    help = 'Fetch opportunities from active RSS sources.'

    def handle(self, *args, **options):

        sources = OpportunitySource.objects.filter(
            is_active=True,
            source_type=OpportunitySource.RSS,
        ).exclude(feed_url='')

        if not sources.exists():
            self.stdout.write(
                self.style.WARNING(
                    'No active RSS sources with feed URLs found.'
                )
            )
            return

        total_created = 0
        total_failed = 0

        for source in sources:

            self.stdout.write(
                f'\nChecking: {source.name}'
            )

            try:

                parsed_url = urlparse(source.feed_url)

                if parsed_url.scheme not in ('http', 'https'):
                    raise ValueError('Invalid RSS feed URL.')

                feed = fetch_feed(source.feed_url)

                if feed.bozo and not feed.entries:
                    raise ValueError(
                        str(feed.bozo_exception)
                    )

                if feed.bozo:
                    self.stdout.write(
                        self.style.WARNING(
                            'Warning: Feed contains formatting errors. '
                            'Processing available entries.'
                        )
                    )

                created_count = 0
                duplicate_count = 0

                for entry in feed.entries:

                    title = strip_tags(
                        entry.get('title', '')
                    ).strip()

                    link = entry.get('link', '').strip()

                    if not title or not link:
                        continue

                    link_scheme = urlparse(link).scheme

                    if link_scheme not in ('http', 'https'):
                        continue

                    external_id = str(
                        entry.get('id')
                        or entry.get('guid')
                        or link
                    )[:255]

                    raw_description = (
                        entry.get('summary')
                        or entry.get('description')
                        or ''
                    )

                    description = strip_tags(
                        raw_description
                    ).strip()

                    category = detect_category(
                        title,
                        description
                    )

                    published_date = get_published_date(entry)

                    try:

                        opportunity, created = (
                            Opportunity.objects.get_or_create(
                                source=source,
                                external_id=external_id,
                                defaults={
                                    'title': title[:250],
                                    'organisation': source.name[:200],
                                    'category': category,
                                    'description': description or title,
                                    'application_url': link,
                                    'source_url': link,
                                    'date_posted': published_date,
                                    'discovered_at': timezone.now(),
                                    'status': Opportunity.PENDING_REVIEW,
                                }
                            )
                        )

                        if created:
                            created_count += 1

                        else:
                            duplicate_count += 1

                    except IntegrityError:
                        duplicate_count += 1

                        continue

                source.last_checked_at = timezone.now()

                source.save(
                    update_fields=['last_checked_at']
                )

                total_created += created_count

                self.stdout.write(
                    self.style.SUCCESS(
                        f'{source.name}: '
                        f'{created_count} new opportunities found.'
                    )
                )

                self.stdout.write(
                    f'Duplicates skipped: {duplicate_count}'
                )

            except (URLError, TimeoutError, OSError, ValueError) as error:

                total_failed += 1

                self.stderr.write(
                    self.style.ERROR(
                        f'Error checking {source.name}: {error}'
                    )
                )

            except Exception as error:

                total_failed += 1

                self.stderr.write(
                    self.style.ERROR(
                        f'Unexpected error checking '
                        f'{source.name}: {error}'
                    )
                )

        self.stdout.write('\n' + '=' * 45)

        self.stdout.write(
            self.style.SUCCESS(
                f'Finished. Total new opportunities: {total_created}'
            )
        )

        self.stdout.write(
            f'Sources that failed: {total_failed}'
        )