from rest_framework import viewsets
from Trips.serializers import TripSerializer
from Trips.models import Trip
from rest_framework.generics import RetrieveAPIView
from helper.choices import TRIP_CATEGORIES
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'distance': ['gte', 'lte'],
        'address_from': ['exact', 'icontains'],  
        'address_to': ['exact', 'icontains'],  
        'category': ['exact', 'icontains'],  
        'date': ['gte', 'lte'], 
    }
    search_fields = ['title', 'category', 'address_from', 'address_to']
    ordering_fields = ['distance']  
    
    def get_queryset(self):
        if self.action == 'list':
            queryset = Trip.objects.all().order_by('-date')
            # queryset = queryset.exclude(user = self.request.user)
            return queryset 
        return super().get_queryset()


class TripCategoriesView(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    
    def get(self, request):
        categories = []
        for category_slug, category_name in dict(TRIP_CATEGORIES).items():
            categories.append({
                'label': category_name,
                'value': category_slug,
            })
        return Response(categories)