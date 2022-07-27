from rest_framework import routers
from .views import LicenseReadViewSet

router = routers.SimpleRouter()
router.register(r'detect',LicenseReadViewSet, basename='npr')

urlpatterns = router.urls
