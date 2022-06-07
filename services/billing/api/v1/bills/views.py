from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.bills.serializers import (
    BillAutoPaySerializer,
    BillConfirmUrlSerializer,
    BillCreateRequestSerializer,
    BillListSerializer,
    YooKassaNotificationSerializer,
)
from billing.repositories.bill import BillRepository


class BillViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=BillListSerializer)
    def list(self, request: Request) -> Response:
        user_uuid: str = request.user.id
        bills = BillRepository.get_user_bills(user_uuid=user_uuid)
        return Response(BillListSerializer(bills, many=True).data)

    @extend_schema(request=YooKassaNotificationSerializer)
    @action(methods=["POST"], permission_classes=[AllowAny], detail=False)
    def notification_url(self, request: Request) -> Response:
        data = request.data
        # TODO: обрабатывать ответ из YooKassa
        return Response(data)

    @extend_schema(
        request=BillCreateRequestSerializer,
        responses={
            201: BillConfirmUrlSerializer,
            200: BillAutoPaySerializer,
            400: BillAutoPaySerializer,
        },
    )
    def create(self, request: Request) -> Response:
        http_status = status.HTTP_200_OK
        result: dict = BillRepository.buy_item(request=request)
        if result.get("confirmation_url"):
            serializer = BillConfirmUrlSerializer(result)
            return Response(data=serializer.data, status=http_status)
        else:
            serializer = BillAutoPaySerializer(result)
            if result.get("is_successful") is False:
                http_status = status.HTTP_400_BAD_REQUEST
            return Response(data=serializer.data, status=http_status)
