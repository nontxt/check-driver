from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_409_CONFLICT

from . import serializers
from .models import Printer, Check


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
    serializer = serializers.OrderSerializer(data=request.data)
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

    check_serializer = serializers.CheckSerializer(data=data, many=True)
    if check_serializer.is_valid(raise_exception=True):
        check_serializer.save()
        return Response({'message': 'Order has been created.'})
