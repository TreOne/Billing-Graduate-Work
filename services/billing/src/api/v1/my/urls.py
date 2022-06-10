from rest_framework.routers import DefaultRouter

from api.v1.my.bills.views import MyBillViewSet

router = DefaultRouter()
router.register('bills', MyBillViewSet, basename='bills')

urlpatterns = []

urlpatterns += router.urls
