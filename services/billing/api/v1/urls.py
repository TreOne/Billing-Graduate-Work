from rest_framework.routers import DefaultRouter

from api.v1.bills.views import BillViewSet

router = DefaultRouter()
router.register("bills", BillViewSet, basename="bills")

urlpatterns = []

urlpatterns += router.urls
