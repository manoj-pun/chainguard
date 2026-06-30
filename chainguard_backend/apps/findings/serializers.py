from rest_framework import serializers
from .models import Finding

"""Serializer for creating findings"""
class FindingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = ["evidence", "content"]


"""Serializer for listing findings"""
class FindingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = ["finding_id", "evidence", "version_number", "created_at"]


"""Serializer for listing findings with id"""
class FindingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = ["finding_id", "evidence", "analyst", "content", "version_number", "created_at"]
        read_only_fields = ["finding_id", "analyst", "version_number", "created_at"]