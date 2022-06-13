import logging

from rest_framework import serializers

from billing.models import Bill
from billing.models.enums import BillType

logger = logging.getLogger('billing')


class BillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            'type',
            'item_uuid',
        )

    def validate(self, data):
        filters: dict = {
            'user_uuid': self.context['user_uuid'],
            'item_uuid': data['item_uuid'],
            'type': BillType.movie,
        }
        if self.Meta.model.objects.filter(**filters).exists():
            logger.info('The user tries to re-purchase the movie.', extra=filters)
            raise serializers.ValidationError({'detail': 'You have already bought this movie.'})
        return data


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
            'id': '22d6d597-000f-5000-9000-145f6df21d6f',
            'status': 'succeeded',
            'paid': True,
            'amount': {'value': '70.00', 'currency': 'RUB'},
            'authorization_details': {
                'rrn': '10000000000',
                'auth_code': '000000',
                'three_d_secure': {'applied': True},
            },
            'created_at': '2018-07-10T14:27:54.691Z',
            'description': 'Заказ №72',
            'expires_at': '2018-07-17T14:28:32.484Z',
            'metadata': {},
            'payment_method': {
                'type': 'bank_card',
                'id': '22d6d597-000f-5000-9000-145f6df21d6f',
                'saved': False,
                'card': {
                    'first6': '555555',
                    'last4': '4444',
                    'expiry_month': '07',
                    'expiry_year': '2021',
                    'card_type': 'MasterCard',
                    'issuer_country': 'RU',
                    'issuer_name': 'Sberbank',
                },
                'title': 'Bank card *4444',
            },
            'refundable': False,
            'test': False,
        }
    )
