import uuid
from django.db import models

def evidence_upload_path(instance, filename):
    return f"evidencefile/{instance.evidence_id}/{instance.file_type}/{filename}"

class Evidence(models.Model):
    class Status(models.TextChoices):
        COLLECTED = "COLLECTED", "Collected"
        IN_STORAGE = "IN_STORAGE", "In Storage"
        WITH_ANALYST = "WITH_ANALYST", "With Analyst"
        ANALYSIS_COMPLETE = "ANALYSIS_COMPLETE", "Analysis Complete"

    evidence_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey('cases.Case', on_delete=models.PROTECT, related_name="case_evidence_items")
    officer = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name="officer_evidence_items")
    description = models.TextField()
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.COLLECTED)
    submitted_to_storage_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Evidence [{self.status}] — {self.case.title}"
    
    class Meta:
        db_table = "evidence"


class EvidenceFile(models.Model):
    class FileType(models.TextChoices):
        IMAGE = "IMAGE","Image"
        VIDEO = "VIDEO", "Video"
        DOCUMENT = "DOCUMENT", "Document"

    evidence_file_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    evidence = models.ForeignKey(Evidence,on_delete=models.PROTECT,related_name="evidence_files")
    file = models.FileField(upload_to=evidence_upload_path)
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    sha256_hash = models.CharField(max_length=64, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} — {self.evidence}"
    
    #hash the file before saving
    def save(self, *args, **kwargs):
        from .utils import generate_hash
        if self._state.adding: #only generate hash if only a new evidence is inserted
            self.sha256_hash = generate_hash(self.file)
        else:
            raise ValueError("EvidenceFile cannot be modified after upload.")
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = "evidence_files"