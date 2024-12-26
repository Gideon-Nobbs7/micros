from django.urls import path, include
from .views import FareViewset, UserAPIView

urlpatterns = [
    path("fares", FareViewset.as_view({
        'get':'list',
        'post':'create'
    })),
    path("fares/<str:pk>", FareViewset.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path("user", UserAPIView.as_view())
]