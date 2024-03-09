from rest_framework.response import Response
from rest_framework.views import APIView
from Explore.serializers import SampleTripSerializer
from .models import TripSample

countries_info = {
    'Australia': {
        'Location': 'Oceania',
        'Capital': 'Canberra',
        'Known_for': 'Great Barrier Reef, Sydney Opera House, unique wildlife'
    },
    'Canada': {
        'Location': 'North America',
        'Capital': 'Ottawa',
        'Known_for': 'Beautiful landscapes, maple syrup, diverse cities'
    },
    'China': {
        'Location': 'East Asia',
        'Capital': 'Beijing',
        'Known_for': 'Great Wall of China, Terracotta Army, rich history and culture'
    },
    'Egypt': {
        'Location': 'North Africa',
        'Capital': 'Cairo',
        'Known_for': 'Pyramids of Giza, Sphinx, ancient history'
    },
    'France': {
        'Location': 'Western Europe',
        'Capital': 'Paris',
        'Known_for': 'Eiffel Tower, Louvre Museum, cuisine, art, and fashion'
    },
    'Germany': {
        'Location': 'Central Europe',
        'Capital': 'Berlin',
        'Known_for': 'Efficient engineering, historical sites, Oktoberfest'
    },
    'Hawaii': {
        'Location': 'United States (Pacific)',
        'Capital': 'Honolulu',
        'Known_for': 'Beautiful beaches, volcanic landscapes, hula dancing'
    },
    'Iceland': {
        'Location': 'North Atlantic',
        'Capital': 'Reykjavik',
        'Known_for': 'Geysers, glaciers, Northern Lights'
    },
    'India': {
        'Location': 'South Asia',
        'Capital': 'New Delhi',
        'Known_for': 'Taj Mahal, diverse cultures, spirituality'
    },
    'Indonesia': {
        'Location': 'Southeast Asia',
        'Capital': 'Jakarta',
        'Known_for': 'Bali, diverse islands, rich biodiversity'
    },
    'Italy': {
        'Location': 'Southern Europe',
        'Capital': 'Rome',
        'Known_for': 'Colosseum, Venice canals, art, and cuisine'
    },
    'Japan': {
        'Location': 'East Asia',
        'Capital': 'Tokyo',
        'Known_for': 'Cherry blossoms, advanced technology, traditional culture'
    },
    'Mexico': {
        'Location': 'North America',
        'Capital': 'Mexico City',
        'Known_for': 'Ancient ruins (Chichen Itza), vibrant culture, cuisine'
    },
    'Russia': {
        'Location': 'Eastern Europe / Northern Asia',
        'Capital': 'Moscow',
        'Known_for': 'Red Square, Trans-Siberian Railway, rich history'
    },
    'Singapore': {
        'Location': 'Southeast Asia',
        'Capital': 'Singapore City',
        'Known_for': 'Modern architecture, cleanliness, diverse cuisine'
    },
    'Spain': {
        'Location': 'Southern Europe',
        'Capital': 'Madrid',
        'Known_for': 'Flamenco dancing, historic landmarks, beaches'
    },
    'Switzerland': {
        'Location': 'Central Europe',
        'Capital': 'Bern',
        'Known_for': 'Alps, chocolate, precision watchmaking'
    },
    'Thailand': {
        'Location': 'Southeast Asia',
        'Capital': 'Bangkok',
        'Known_for': 'Temples, beaches, vibrant street life'
    },
    'Turkey': {
        'Location': 'Western Asia / Southeast Europe',
        'Capital': 'Ankara',
        'Known_for': 'Hagia Sophia, Grand Bazaar, unique blend of cultures'
    },
    'Usa': {
        'Location': 'North America',
        'Capital': 'Washington, D.C.',
        'Known_for': 'Statue of Liberty, Yellowstone National Park, diverse cities'
    },
    # 'World': {
    #     'Info': 'This likely refers to global or international contexts rather than a specific country.'
    # }
}


class TripSampleDataView(APIView):
    def get(self, request, category=None):
        sample_qry = TripSample.objects.filter(category = category)
        sample_trip_data = SampleTripSerializer(sample_qry,many=True).data
        return Response(sample_trip_data)
    
    
class TripSampleCategoryView(APIView):
    def get(self, request):
        categories = TripSample.objects.values_list('category', flat=True).order_by('category').distinct()
        data = []
        for category in categories:
            data.append(
                {
                    'category': category,
                    'label': category.title(),
                    'cover' : TripSample.objects.filter(category = category).order_by('?').first().image_url,
                    'hover_data' : countries_info.get(category.title())
                }
            )            
        return Response(data)
