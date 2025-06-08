from rest_framework import serializers
from shop.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ['creator_id', 'answer', 'is_blocked', 'created_at', 'updated_at']


class FeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedback_id', 'feedback']


class AdminAnswerSerializer(serializers.Serializer):
    feedback_id = serializers.IntegerField()
    answer = serializers.CharField()


class AdminBlockSerializer(serializers.Serializer):
    feedback_id = serializers.IntegerField()
    is_blocked = serializers.BooleanField()
