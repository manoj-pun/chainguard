from django.db import transaction
from .models import Finding
from apps.audits.models import AuditLog

"""Services for creating findings"""
def create_finding(*, evidence, analyst, content):
    with transaction.atomic():
        last_version = (
            Finding.objects.select_for_update()
            .filter(evidence=evidence)
            .order_by('-version_number')
            .first()
        )
        next_version = (last_version.version_number + 1) if last_version else 1

        finding = Finding.objects.create(
            evidence=evidence,
            analyst=analyst,
            content=content,
            version_number=next_version,
        )

        AuditLog.objects.create(
            actor=analyst,
            action=AuditLog.Action.FINDING_CREATED,
            entity_type="Finding",
            entity_id=str(finding.pk),
        )

        return finding