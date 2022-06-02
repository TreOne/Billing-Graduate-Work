from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.v1.subscriptions.serializers import SubscriptionSerializer
from billing.models import Subscription


# @method_decorator(response_wrapper(), name="dispatch")
class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (AllowAny,)
