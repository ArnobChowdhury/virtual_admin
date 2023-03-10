from gadgets.views import DeviceViewSet, ApplicationViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='devices')
router.register(r'applications', ApplicationViewSet, basename='applications')

urlpatterns = router.urls
