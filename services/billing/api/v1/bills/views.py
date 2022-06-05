from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.bills.serializers import (
    BillConfirmUrlSerializer,
    BillCreateRequestSerializer,
    BillCreateSerializer,
    BillListSerializer,
)
from billing.models.enums import BillType
from billing.repositories import BillRepository, SubscriptionRepository, UserAutoPayRepository
from config.payment_service import payment_system
from utils.schemas import PaymentParams


class BillViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=BillListSerializer)
    def list(self, request: Request) -> Response:
        user_uuid: str = request.user.id
        bills = BillRepository.get_user_bills(user_uuid=user_uuid)
        return Response(BillListSerializer(bills, many=True).data)

    @extend_schema(
        request=BillCreateRequestSerializer, responses=BillConfirmUrlSerializer
    )
    def create(self, request: Request) -> Response:
        user_uuid: str = request.user.id
        autopay_id = None
        request_serializer = BillCreateRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer = request_serializer.save()
        item_uuid: str = request_serializer.get("item_uuid")
        bill_type: str = request_serializer.get("type")

        if bill_type == BillType.subscription:
            subscription = SubscriptionRepository.get_by_id(item_uuid=item_uuid)
            amount = subscription.price
            autopay_id = UserAutoPayRepository.get_users_auto_pay(user_uuid=user_uuid)
        elif bill_type == BillType.movie:
            # TODO: стучаться на сервис с фильмами и получать информацию
            movie_title: str = ''
            raise NotFound
        else:
            raise NotFound

        serializer = BillCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save(user_uuid=user_uuid, amount=amount)

        description: str = ""
        save_payment_method: bool = False
        if bill_type == BillType.subscription:
            save_payment_method: bool = True
            description: str = f"У вас теперь есть {bill.type} '{subscription.title}'."
        elif bill_type == BillType.movie:
            description: str = f"У вас теперь есть {bill.type} '{movie_title}'."

        payment_params = PaymentParams(
            bill_uuid=str(bill.id),
            amount=bill.amount,
            description=description,
            save_payment_method=save_payment_method,
            autopay_id=autopay_id
        )
        confirmation_url = payment_system.create_confirmation_url(params=payment_params)
        return Response(
            BillConfirmUrlSerializer({"confirmation_url": confirmation_url}).data,
            status=status.HTTP_201_CREATED,
        )
