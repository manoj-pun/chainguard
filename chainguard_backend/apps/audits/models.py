from django.db import models
import uuid

class AuditLog(models.Model):
    class Action(models.TextChoices):
        CASE_CREATED = "CASE_CREATED", "Case Created"
        CASE_SUBMITTED_TO_STORAGE = "CASE_SUBMITTED_TO_STORAGE", "Case Submitted to Storage"
        CASE_IN_STORAGE = "CASE_IN_STORAGE", "Case In Storage"
        CASE_WITH_ANALYST = "CASE_WITH_ANALYST", "Case With Analyst"
        CASE_UNDER_REVIEW = "CASE_UNDER_REVIEW", "Case Under Review"
        CASE_SENT_TO_COURT = "CASE_SENT_TO_COURT", "Case Sent to Court"
        CASE_CLOSED = "CASE_CLOSED", "Case Closed"
        EVIDENCE_COLLECTED = "EVIDENCE_COLLECTED", "Evidence Collected"
        EVIDENCE_FILE_UPLOADED = "EVIDENCE_FILE_UPLOADED", "Evidence File Uploaded"
        EVIDENCE_ANALYSIS_COMPLETE = "EVIDENCE_ANALYSIS_COMPLETE", "Evidence Analysis Complete"
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="audit_logs")
    action = models.CharField(max_length=100, choices=Action.choices)
    entity_type = models.CharField(max_length=50)   # e.g. "Case", "Evidence"
    entity_id = models.CharField(max_length=36)   # UUID stored as string
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audits"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["actor"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.actor} → {self.action} on {self.entity_type}:{self.entity_id}"
