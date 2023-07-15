from django.db import models
from decimal import Decimal

CHECK_TYPES = (
    ('kit', 'kitchen'),
    ('cli', 'client'),
)

STATUS = (
    ('n', 'new'),
    ('r', 'rendered'),
    ('p', 'printed'),
)


class Printer(models.Model):
    name = models.CharField(max_length=200)
    api_key = models.CharField(unique=True)
    check_type = models.CharField(choices=CHECK_TYPES)
    point_id = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='checks')
    type = models.CharField(choices=CHECK_TYPES)
    order = models.JSONField(default=dict)
    status = models.CharField(choices=STATUS, default='n')
    pdf_file = models.FileField(blank=True, upload_to='pdf', )

    def __str__(self):
        order_id = self.order.get('order_id', None)
        return f'Order №{order_id}'

    def get_total_cost(self):
        return Decimal(sum([item['cost'] for item in self.order.get('items')]))

