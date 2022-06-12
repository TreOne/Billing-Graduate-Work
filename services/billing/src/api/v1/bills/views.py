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
    YooKassaNotificationSerializer,
)
from billing.models.enums import BillStatus
from billing.repositories.bill import BillRepository
from billing.repositories.user_autopay import UserAutoPayRepository
from utils.schemas.bill import BillBaseSchema


class BillViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=YooKassaNotificationSerializer,
        description='Хук для уведомлений с YooKassa',
        tags=['yookassa'],
    )
    @action(methods=['POST'], permission_classes=[AllowAny], detail=False)
    def yookassa_notification_url(self, request: Request) -> Response:
        """Обработка уведомления об изменениях статуса Оплаты из сервиса Yookassa."""
        yookassa_object: dict = request.data['object']
        payment_id: str = yookassa_object['payment_method']['id']
        bill_uuid: str = yookassa_object['metadata']['bill_uuid']
        is_token_saved: bool = yookassa_object['payment_method']['saved']
        bill_status: str = BillRepository.determine_bill_status(
            bill_status=yookassa_object['status']
        )
        three_d_secure: bool = yookassa_object['authorization_details']['three_d_secure'][
            'applied'
        ]

        if all((is_token_saved, bill_status == BillStatus.paid, three_d_secure is False)):
            # save User's auto pay
            bill_instance = BillRepository.get_by_id(item_uuid=bill_uuid)
            UserAutoPayRepository.save_users_auto_pay(
                payment_id=payment_id, user_uuid=bill_instance.user_uuid,
            )
        BillRepository.update_bill_status(bill_uuid=bill_uuid, bill_status=bill_status)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=BillCreateRequestSerializer,
        responses={
            201: BillConfirmUrlSerializer,
            200: BillAutoPaySerializer,
            400: BillAutoPaySerializer,
        },
        tags=['bills'],
    )
    def create(self, request: Request) -> Response:
        """Метод на покупку фильмов и подписок."""
        request_serializer = BillCreateRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer = request_serializer.save()

        user_uuid: str = request.user.id
        item_uuid: str = request_serializer.get('item_uuid')
        bill_type: str = request_serializer.get('type')

        bill_schema: BillBaseSchema = BillBaseSchema(
            **{'user_uuid': user_uuid, 'type': bill_type, 'item_uuid': item_uuid, }
        )
        result: dict = BillRepository.buy_item(bill_schema=bill_schema)

        http_status = status.HTTP_200_OK
        if result.get('confirmation_url'):
            serializer = BillConfirmUrlSerializer(result)
            return Response(data=serializer.data, status=http_status)
        else:
            serializer = BillAutoPaySerializer(result)
            if result.get('is_successful') is False:
                http_status = status.HTTP_400_BAD_REQUEST
            return Response(data=serializer.data, status=http_status)
