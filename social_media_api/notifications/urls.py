from django.urls import path, include
from .views import Notification 

router = DefaultRouter()
router.register(r'notification',/notification/)

urlpatterns = [
    path('api/', include(router.urls)), 
]
