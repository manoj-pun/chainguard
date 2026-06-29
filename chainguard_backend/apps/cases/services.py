from .models import Case
from apps.audits.models import AuditLog
from django.db import transaction

"""Create case services"""
@transaction.atomic
def create_case(*, officer, validated_data):
    case = Case.objects.create(
        officer = officer,
        **validated_data
    )

    # raise Exception("Testing rollback")  

    AuditLog.objects.create(
        actor = officer,
        action = AuditLog.Action.CASE_CREATED,
        entity_type = "Case",
        entity_id = str(case.pk)
    )

    return case