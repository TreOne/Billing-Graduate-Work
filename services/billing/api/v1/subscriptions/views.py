from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.v1.subscriptions.serializers import SubscriptionSerializer
from billing.repositories import SubscriptionRepository


# @method_decorator(response_wrapper(), name="dispatch")
class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = SubscriptionRepository.get_all()
    serializer_class = SubscriptionSerializer
    permission_classes = (AllowAny,)
