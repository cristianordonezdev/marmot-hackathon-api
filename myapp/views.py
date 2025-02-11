from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = (MultiPartParser, FormParser)