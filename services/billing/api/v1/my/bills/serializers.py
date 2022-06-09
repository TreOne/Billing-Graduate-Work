from rest_framework import serializers

from billing.models import Bill


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
