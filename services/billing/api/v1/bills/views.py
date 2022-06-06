from typing import Optional

from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.bills.serializers import (
    BillConfirmUrlSerializer,
    BillCreateRequestSerializer,
    BillCreateSerializer,
    BillListSerializer,
    YooKassaNotificationSerializer,
)
from billing.models.enums import BillType
from billing.repositories import (
    BillRepository,
    SubscriptionRepository,
    UserAutoPayRepository,
    MovieRepository,
)
from config.payment_service import payment_system
from utils.schemas import PaymentParams


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
        request=BillCreateRequestSerializer, responses=BillConfirmUrlSerializer
    )
    def create(self, request: Request) -> Response:
        user_uuid: str = request.user.id
        autopay_id: Optional[str] = UserAutoPayRepository.get_users_auto_pay(user_uuid=user_uuid)
        request_serializer = BillCreateRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer = request_serializer.save()
        item_uuid: str = request_serializer.get("item_uuid")
        bill_type: str = request_serializer.get("type")

        if bill_type == BillType.subscription:
            subscription = SubscriptionRepository.get_by_id(item_uuid=item_uuid)
            amount = subscription.get('price')
            description: str = f"У вас теперь есть {bill_type} '{subscription.get('title')}'."
        elif bill_type == BillType.movie:
            movie_title, amount = MovieRepository.get_by_id(item_uuid=item_uuid)
            description: str = f"У вас теперь есть {bill_type} '{movie_title}'."
        else:
            raise NotFound

        serializer = BillCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save(user_uuid=user_uuid, amount=amount)

        payment_params = PaymentParams(
            bill_uuid=str(bill.id),
            amount=bill.amount,
            description=description,
            save_payment_method=True,
            autopay_id=autopay_id
        )
        confirmation_url = payment_system.create_confirmation_url(params=payment_params)
        return Response(
            BillConfirmUrlSerializer({"confirmation_url": confirmation_url}).data,
            status=status.HTTP_201_CREATED,
        )
