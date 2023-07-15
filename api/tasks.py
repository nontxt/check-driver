import weasyprint

from celery import shared_task

from django.template.loader import render_to_string
from django.conf import settings

from .models import Check


@shared_task
def render_pdf(check_id: int):
    """
    Take check_id and rendering PDF from HTML for this
    """
    check = Check.objects.get(id=check_id)
    order = check.order
    order_id = order.get('order_id')
    check_type = check.get_type_display()   # human-readable type of check

    filename = f'{order_id}_{check_type}.pdf'
    html = render_to_string('pdf.html', {'check': check, 'order_id': order_id, 'items': order.get('items')})
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]

    with open(settings.MEDIA_ROOT / filename, 'wb') as file:
        file.write(weasyprint.HTML(string=html).write_pdf(stylesheets=stylesheets))

    check.pdf_file.name = filename  # set file to FileField
    check.status = 'r'
    check.save()
