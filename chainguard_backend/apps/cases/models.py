import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Case(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        SUBMITTED_TO_STORAGE = "SUBMITTED_TO_STORAGE", "Submitted to Storage"
        IN_STORAGE = "IN_STORAGE", "In Storage"
        WITH_ANALYST = "WITH_ANALYST", "With Analyst"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        SENT_TO_COURT = "SENT_TO_COURT", "Sent to Court"
        CLOSED = "CLOSED", "Closed"

    case_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    officer = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name="cases")
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "cases"