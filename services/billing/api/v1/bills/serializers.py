from uuid import UUID

from rest_framework import serializers

from billing.models import Bill
from billing.models.enums import BillType


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ("id",)


class BillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            "type",
            "item_uuid",
        )


class BillCreateRequestSerializer(serializers.Serializer):
    # item_uuid = serializers.UUIDField(required=True)
    item_uuid = serializers.UUIDField(
        default=UUID("5933beb6-383a-4de0-bca5-836493024c71")
    )
    type = serializers.CharField(default=BillType.subscription)

    def create(self, validated_data) -> dict:
        return validated_data


class BillConfirmUrlSerializer(serializers.Serializer):
    confirmation_url = serializers.CharField()
