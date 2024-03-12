from django.urls import path
from Extra.views import PingsListView, PingsSetSeenView


urlpatterns = [
    path('pings', PingsListView.as_view()),
    path('pings-set-seen', PingsSetSeenView.as_view())
]
