from rest_framework import serializers

from billing.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "id",
            "title",
            "price",
            "description",
        )
