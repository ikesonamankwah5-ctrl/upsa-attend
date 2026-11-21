from django.http import HttpResponse
from django.conf import settings
from pathlib import Path


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