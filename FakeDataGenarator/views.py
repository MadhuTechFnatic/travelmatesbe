from rest_framework.response import Response
from rest_framework.views import APIView
from Explore.models import TripSample
import json
from Trips.models import Trip
from FakeDataGenarator.fake_data import fake_trips
from Users.models import User
import requests
from django.core.files.base import ContentFile

class ExploreTripSampleData(APIView):
    def get(self, request):

        with open('trips.json', 'r', encoding='utf-8') as file:
            trip_sample_data = json.load(file)

        for trip_sample in trip_sample_data:
            modal_data = {
                'title': ''.join(trip_sample['title'].split('. ')[1:]),
                'content': trip_sample['content'],
                'image_url': trip_sample['image'],
                'category': trip_sample['contry'],
            }
            TripSample.objects.create(**modal_data)
        # return Response(modal_data)
        return Response('Fake Data is available now for Explore Trip Sample')


class TripsFakeData(APIView):
    def get(self, request):
        Trip.objects.all().delete()  # This line will delete all existing trips in each iteration. Consider moving it outside the loop if you only want to delete them once.
        for trip_data in fake_trips:
            response = requests.get(trip_data['trip_cover_img'])
            trip_data['user'] = User.objects.get(email=trip_data['user'])
        
            trip = Trip(
                user=trip_data['user'],
                title=trip_data['title'],
                address_from=trip_data['address_from'],
                address_to=trip_data['address_to'],
                category=trip_data['category'],
                date=trip_data['date'],
                time=trip_data['time'],
                group_size=trip_data['group_size'],
                distance=trip_data['distance'],
                description=trip_data['description'],
            )
            
            # Save the image to the trip_cover_img field if available
            if response.status_code == 200:
                try:
                    trip.trip_cover_img.save(f"{trip_data['title']}.jpg", ContentFile(response.content), save=True)
                except Exception as e:
                    print(f"An error occurred while saving image for trip: {trip_data['title']}: {str(e)}")
                    pass  # Skip saving the image and continue with the remaining details
            
            # Save the trip object
            trip.save()
            print(trip)
        
        return Response('Trips are available now for testing')
