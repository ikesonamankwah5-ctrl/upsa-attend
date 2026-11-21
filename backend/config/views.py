from pathlib import Path

from django.conf import settings
from django.contrib import admin, messages
from django.core.management import call_command, CommandError
from django.http import HttpResponse
from django.shortcuts import render, redirect


def service_worker(request):
    sw_path = Path(settings.BASE_DIR) / 'static' / 'pwa' / 'sw.js'

    try:
        content = sw_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return HttpResponse(
            'Service worker not found.',
            status=404
        )

    response = HttpResponse(
        content,
        content_type='application/javascript'
    )
    response['Cache-Control'] = 'no-cache'
    response['Service-Worker-Allowed'] = '/'

    return response


@admin.site.admin_view
def restore_career_catalogue(request):

    if request.method == 'POST':
        try:
            call_command('restore_career_catalogue')

            messages.success(
                request,
                'Career Catalogue and Career Quest restoration completed.'
            )

        except CommandError as error:
            messages.error(request, str(error))

        except Exception:
            messages.error(
                request,
                'An unexpected error occurred during restoration. '
                'Check the deployment logs.'
            )

        return redirect('restore_career_catalogue')

    context = admin.site.each_context(request)
    context['title'] = 'Restore Career Catalogue'

    return render(
        request,
        'admin/restore_career_catalogue.html',
        context
    )