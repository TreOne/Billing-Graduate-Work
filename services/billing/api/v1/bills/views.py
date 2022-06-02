from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.bills.serializers import BillSerializer
from billing.models import Bill


# @method_decorator(response_wrapper(), name="dispatch")
class BillViewSet(viewsets.ModelViewSet):

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticated,)
