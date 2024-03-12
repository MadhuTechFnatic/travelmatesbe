from rest_framework.generics import ListAPIView, UpdateAPIView
from Extra.serializers import PingSerializer
from Extra.models import Ping
from rest_framework.response import Response


class PingsListView(ListAPIView):
    serializer_class = PingSerializer
    queryset = Ping.objects.all()
    
    def get(self, request):
        user = request.user
        pings = Ping.objects.filter(user=user, is_seen = False)
        data = self.get_serializer(pings, many = True).data
        return Response(data, 200)
    
    
class PingsSetSeenView(UpdateAPIView):
    serializer_class = PingSerializer
    queryset = Ping.objects.all()
    
    def update(self, request):
        user = request.user
        pings = Ping.objects.filter(user=user, is_seen = False)
        pings.update(is_seen = True)
        return Response(None, 200)
    
    
    