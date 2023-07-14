from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.status import HTTP_409_CONFLICT

from . import serializers, models
from .models import Printer, Check


@api_view(['POST'])
def create_order(request):
    serializer = serializers.OrderSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    order_id = request.data.get('order_id')
    if Check.objects.filter(pdf_file__startswith=f'pdf/{order_id}_').exists():
        return Response(
            {'message': 'Checks for order already exists.', 'order': order_id},
            status=HTTP_409_CONFLICT)

    point_id = request.data.get('point_id')
    printers = Printer.objects.filter(point_id=point_id)
    if len(printers) == 0:
        raise NotFound(f'Point {point_id} has not any printers')

    data = []
    for printer in printers:
        data.append({
            'printer_id': printer.id,
            'type': printer.check_type,
            'order': request.data,
        })

    check_serializer = serializers.CheckSerializer(data=data, many=True)
    if check_serializer.is_valid(raise_exception=True):
        check_serializer.save()
        return Response({'message': 'Order has been created.'})
