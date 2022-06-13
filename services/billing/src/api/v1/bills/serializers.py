import logging

from rest_framework import serializers

from billing.models.enums import BillType

logger = logging.getLogger('billing')


class BillCreateRequestSerializer(serializers.Serializer):
    item_uuid = serializers.CharField(default='065ad9e0-bb75-4127-94a6-6022e3e0a666')
    type = serializers.CharField(default=BillType.subscription)

    def create(self, validated_data) -> dict:
        return validated_data


class BillConfirmUrlSerializer(serializers.Serializer):
    confirmation_url = serializers.CharField()


class BillAutoPaySerializer(serializers.Serializer):
    message = serializers.CharField()


class YooKassaNotificationSerializer(serializers.Serializer):
    type = serializers.CharField(default='notification')
    event = serializers.CharField(default='payment.succeeded')
    object = serializers.JSONField(
        default={
            'id': '2a386ba4-000f-5000-8000-16ffa705ce61',
            'status': 'succeeded',
            'amount': {'value': '400.00', 'currency': 'RUB'},
            'income_amount': {'value': '386.00', 'currency': 'RUB'},
            'description': "Оплата подписки 'Practix.Стандарт'.",
            'recipient': {'account_id': '912730', 'gateway_id': '1973714'},
            'payment_method': {
                'type': 'bank_card',
                'id': '2a386960-000f-5000-a000-18ac5f2e05fa',
                'saved': True,
                'title': 'Bank card *1111',
                'card': {
                    'first6': '411111',
                    'last4': '1111',
                    'expiry_year': '2027',
                    'expiry_month': '11',
                    'card_type': 'Visa',
                    'issuer_country': 'US',
                },
            },
            'captured_at': '2022-06-12T21:17:25.998Z',
            'created_at': '2022-06-12T21:17:25.003Z',
            'test': True,
            'refunded_amount': {'value': '0.00', 'currency': 'RUB'},
            'paid': True,
            'refundable': True,
            'metadata': {'bill_uuid': 'db2d00cf-b6b4-4d90-86e3-4712bc13e969'},
            'authorization_details': {
                'rrn': '348471162165653',
                'auth_code': '145150',
                'three_d_secure': {'applied': False},
            },
        },
    )


class YooKassaRefundNotificationSerializer(serializers.Serializer):
    type = serializers.CharField(default='notification')
    event = serializers.CharField(default='refund.succeeded')
    object = serializers.JSONField(
        default={
            "id": "2a39936f-0015-5000-9000-1614d1c8241f",
            "payment_id": "2a3992a4-000f-5000-9000-156087ef690b",
            "status": "succeeded",
            "created_at": "2022-06-13T18:19:27.838Z",
            "amount": {
                "value": "400.00",
                "currency": "RUB"
            },
        },
    )
