from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, tasks


@receiver(post_save, sender=models.Check)
def render_pdf(sender, instance, created, **kwargs):
    match created, instance.status:
        case True, 'n':  # if check has been created and has status 'new', render PDF
            tasks.render_pdf.delay(instance.id)
        case _:
            pass
