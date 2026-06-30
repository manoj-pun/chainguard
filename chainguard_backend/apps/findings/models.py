from django.db import models
import uuid

class Finding(models.Model):
    class Status(models.TextChoices):
        FINDING_CREATED = "FINDING_CREATED", "Finding Created"
        FINDING_SUBMITTED = "FINDING_SUBMITTED", "Finding Submitted"

    finding_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evidence = models.ForeignKey('evidence.Evidence', on_delete=models.PROTECT, related_name="findings")
    analyst = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name="findings")
    content = models.TextField()
    version_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.FINDING_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "findings"
        constraints = [
            models.UniqueConstraint(
                fields=["evidence", "version_number"],
                name="unique_evidence_version"
            )
        ]