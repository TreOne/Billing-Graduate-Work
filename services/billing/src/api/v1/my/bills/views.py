from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.my.bills.serializers import BillListSerializer
from billing.repositories.bill import BillRepository


class MyBillViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=BillListSerializer)
    def list(self, request: Request) -> Response:
        """Выдача оплат для пользователя."""
        user_uuid: str = request.user.id
        bills = BillRepository.get_user_bills(user_uuid=user_uuid)
        return Response(BillListSerializer(bills, many=True).data)