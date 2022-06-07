from rest_framework import serializers

from billing.models import Bill
from billing.models.enums import BillType


class BillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            "id",
            "status",
            "type",
            "item_uuid",
            "amount",
        )


class BillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            "type",
            "item_uuid",
        )


class BillCreateRequestSerializer(serializers.Serializer):
    item_uuid = serializers.CharField(default="c45ea0ef-f9b4-4569-af09-9ee7b0a9c16c")
    type = serializers.CharField(default=BillType.subscription)

    def create(self, validated_data) -> dict:
        return validated_data


class BillConfirmUrlSerializer(serializers.Serializer):
    confirmation_url = serializers.CharField()


class BillAutoPaySerializer(serializers.Serializer):
    message = serializers.CharField()


class YooKassaNotificationSerializer(serializers.Serializer):
    demo = serializers.CharField(required=True)
