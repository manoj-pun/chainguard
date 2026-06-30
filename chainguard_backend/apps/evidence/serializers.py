from rest_framework import serializers
from .models import Evidence, EvidenceFile

class EvidenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ["case", "description"]


class EvidenceFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceFile
        fields = ["evidence_file_id", "uploaded_at"]


class EvidenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ["evidence_id", "description", "status", "submitted_to_storage_at"]

    
class EvidenceDetailSerializer(serializers.ModelSerializer):
    evidence_files = EvidenceFileListSerializer(many=True)
    class Meta:
        model = Evidence
        fields = ["evidence_id", "description", "status", "evidence_files"]


class EvidenceFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceFile
        fields = ["evidence", "file", "file_type"]


class EvidenceFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceFile
        fields = ["evidence_file_id", "file", "file_type", "sha256_hash", "uploaded_at"]



