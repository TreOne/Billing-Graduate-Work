from rest_framework.routers import DefaultRouter

from api.v1.bills.views import BillViewSet
from api.v1.subscriptions.views import SubscriptionViewSet

router = DefaultRouter()
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")
router.register("bills", BillViewSet, basename="bills")

urlpatterns = []

urlpatterns += router.urls
