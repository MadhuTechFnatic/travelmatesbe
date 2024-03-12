from rest_framework import viewsets
from django.db.models import Q
from Trips.serializers import *
from Trips.models import *
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListCreateAPIView, ListAPIView
from helper.choices import TRIP_CATEGORIES
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
    
    
class TripLikeView(RetrieveAPIView, UpdateAPIView):
    serializer_class = TripLikeSerializer
    queryset = TripLike.objects.all()
    
    def retrieve(self, request, pk):
        trip = Trip.objects.get(pk = pk)
        likes = trip.trip_likes.all()
        if likes.count() == 0:
            return Response([])
        data = self.get_serializer(likes).data
        return Response(data)
    
    def update(self, request, pk):
        status = request.data.get('status')
        trip = Trip.objects.get(pk = pk)
        user = request.user
        if status == None:
            TripLike.objects.get(trip=trip, user=user).delete()   
            like_count = TripLike.objects.filter(trip = trip, user=user, status = 'like').count()           
            dislike_count = TripLike.objects.filter(trip = trip, user=user, status = 'dislike').count()
            return Response({
                'status': status, 
                'like_count' : like_count,
                'dislike_count': dislike_count 
                })

        try:
            like = TripLike.objects.get(trip=trip, user=user)
            like.status = status
            like.save()
            like_count = TripLike.objects.filter(trip = trip, user=user, status = 'like').count()           
            dislike_count = TripLike.objects.filter(trip = trip, user=user, status = 'dislike').count()
            return Response({
                'status': status, 
                'like_count' : like_count,
                'dislike_count': dislike_count 
                })
        except TripLike.DoesNotExist:
            like = TripLike.objects.create(trip=trip, user=user, status = status)
            like_count = TripLike.objects.filter(trip = trip, user=user, status = 'like').count()           
            dislike_count = TripLike.objects.filter(trip = trip, user=user, status = 'dislike').count()
            return Response({
                'status': status, 
                'like_count' : like_count,
                'dislike_count': dislike_count 
                })
 

class TripCommentView(ListCreateAPIView):
    serializer_class = TripCommentSerializer
    queryset = TripComment.objects.all()         
    
    def get(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        comments = trip.trip_comments.all()
        data = self.get_serializer(comments, many = True).data 
        return Response(data, 200)     
    
    def post(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        user = request.user
        comment = request.data.get('comment')
        comment = self.get_queryset().create(user = user, trip = trip, comment = comment)    
        return Response(self.get_serializer(comment).data, 201)
 
    
class TripRequestView(ListCreateAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()         
   
    def get(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        requests = trip.trip_requests.all()
        data = self.get_serializer(requests, many = True).data 
        return Response(data, 200)     
    
    def post(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        user = request.user
        comment = self.get_queryset().create(user = user, trip = trip)    
        return Response(self.get_serializer(comment).data, 201)

    
class TripRequestAcceptRejectView(UpdateAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()    
    
    def update(self, request, request_pk):
        action = request.data.get('action')
        trip_request = self.get_queryset().get(pk = request_pk)
        if action:
            trip_request.is_accepted = True
            trip_request.trip.connected_users.add(trip_request.user)
            trip_request.save()
            return Response({}, 202)
        request.delete()
        return Response({}, 204)
    
    
class UserTripsView(ListAPIView):
    serializer_class = TripSerializer

    def get(self, request, email):
        current_datetime = datetime.datetime.now()
        user = User.objects.get(email=email)

        upcoming_trips = user.user_trips.filter(
            Q(date__gt=current_datetime.date()) | 
            (Q(date=current_datetime.date()) & Q(time__gt=current_datetime.time()))
        )
        completed_trips = user.user_trips.filter(
            Q(date__lt=current_datetime.date()) | 
            (Q(date=current_datetime.date()) & Q(time__lt=current_datetime.time()))
        )

        data = {
            'upcoming_trips': self.get_serializer(upcoming_trips, many=True).data,
            'completed_trips': self.get_serializer(completed_trips, many=True).data,
        }
        return Response(data, status=200)
