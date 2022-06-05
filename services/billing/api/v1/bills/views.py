from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.bills.serializers import BillSerializer
from billing.repositories import SubscriptionRepository


# @method_decorator(response_wrapper(), name="dispatch")
class BillViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):

    queryset = SubscriptionRepository.get_all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticated,)
