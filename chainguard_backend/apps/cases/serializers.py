from rest_framework import serializers
from .models import Case

"""Case Serializer"""
class CaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ["title","description"]

    def validate_title(self,value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must contain at least 5 letters.")
        return value.strip().capitalize()
    

"""List Case Serializer"""
class CaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ["case_id", "title", "description", "status", "created_at", "closed_at"]
        read_only_fields = ["case_id", "created_at", "closed_at"]



