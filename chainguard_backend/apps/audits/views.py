from django.db import models
import uuid

class AuditLog(models.Model):
    
    class Action(models.TextChoices):
        CASE_CREATED        = "CASE_CREATED", "Case Created"
        CASE_UPDATED        = "CASE_UPDATED", "Case Updated"
        CASE_STATUS_CHANGED = "CASE_STATUS_CHANGED", "Case Status Changed"
        EVIDENCE_ADDED      = "EVIDENCE_ADDED", "Evidence Added"
        EVIDENCE_ACCESSED   = "EVIDENCE_ACCESSED", "Evidence Accessed"
        EVIDENCE_TRANSFERRED = "EVIDENCE_TRANSFERRED", "Evidence Transferred"
        FINDING_SUBMITTED   = "FINDING_SUBMITTED", "Finding Submitted"
        FINDING_VERSIONED   = "FINDING_VERSIONED", "Finding Versioned"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    actor = models.ForeignKey("users.User",on_delete=models.PROTECT,null=True,related_name="audit_logs")
    
    action = models.CharField(max_length=50, choices=Action.choices)
    
    entity_type = models.CharField(max_length=50)   # e.g. "Case", "Evidence"
    entity_id   = models.CharField(max_length=36)   # UUID stored as string
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} → {self.action} on {self.entity_type}:{self.entity_id}"