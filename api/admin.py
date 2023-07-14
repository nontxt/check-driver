from django.contrib import admin

from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id',)
    list_filter = ('name', 'check_type', 'point_id',)


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'printer_id', 'type', 'status', 'pdf_file',)
    list_filter = ('printer_id', 'type', 'status',)

    def order_id(self, obj):
        return obj.order.get('order_id', None)
