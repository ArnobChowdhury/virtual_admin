from gadgets.views import DeviceViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='devices')


urlpatterns = router.urls
