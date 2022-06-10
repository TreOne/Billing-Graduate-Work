from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.bills.views import BillViewSet

router = DefaultRouter()
router.register('bills', BillViewSet, basename='bills')

urlpatterns = [
    path('my/', include('api.v1.my.urls')),
]

urlpatterns += router.urls
