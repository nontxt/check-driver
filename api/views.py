from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.viewsets import GenericViewSet

from .serializers import CheckSerializer, OrderSerializer
from .models import Printer, Check


class CheckView(GenericViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    http_method_names = ('post', 'patch')

    def get_queryset(self):
        api_key = self.request.data.get('api_key', None)
        if api_key is None:
            raise ValidationError({'api_key': 'This field is required'})

        queryset = self.queryset
        return queryset.select_related('printer_id').filter(printer_id__api_key=api_key)

    @csrf_exempt
    def pdf(self, request, filename, *args, **kwargs):
        """
        Return PDF file or raise NotFound
        """
        check = self.get_queryset().filter(pdf_file=filename)
        if check.exists():
            file = open(settings.MEDIA_ROOT / filename, 'rb')  # Open the file in binary mode
            return FileResponse(file)
        else:
            raise NotFound()

    def pdf_list(self, request, *args, **kwargs):
        """
        Endpoint that return list of available PDF files in the next format:
        {
            message: ok | empty,
            files: [str, ...] | []
        }
        """
        check_status = request.data.get('check_status', 'r')
        queryset = self.get_queryset().filter(status=check_status)
        pdf_list = queryset.values_list('pdf_file', flat=True)
        data = {
            'message': 'ok' if len(pdf_list) else 'empty',
            'files': pdf_list
        }
        return Response(data)

    def printed(self, request, filename):
        """
        Mark check as 'printed'
        """
        check = get_object_or_404(self.get_queryset(), pdf_file=filename)
        check.status = 'p'
        check.save()
        return Response({'message': 'ok'})


@api_view(['POST'])
def create_order(request):
    """
    Endpoint for creating new order.
    Take next JSON format:
    {
        point_id: int,
        order_id: int,
        items: [
            {name: str, price: float, quantity: int, cost: float},
            ...
        ]
    }
    """
    # Checking payload for correct format
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    point_id = request.data['point_id']
    printers = Printer.objects.filter(point_id=point_id)
    if len(printers) == 0:
        raise NotFound(f'Point {point_id} has not any printers')

    order_id = request.data['order_id']
    if Check.objects.filter(pdf_file__startswith=f'{order_id}_').exists():
        return Response(
            {'message': 'Checks for this order already exists.', 'order': order_id},
            status=HTTP_409_CONFLICT)

    data = []
    for printer in printers:
        data.append({
            'printer_id': printer.id,
            'type': printer.check_type,
            'order': request.data,
        })

    check_serializer = CheckSerializer(data=data, many=True)
    if check_serializer.is_valid(raise_exception=True):
        check_serializer.save()
        return Response({'message': 'Order has been created.'})
