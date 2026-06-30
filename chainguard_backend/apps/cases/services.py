from .models import Case
from apps.audits.models import AuditLog
from django.db import transaction
from django.db.models import Count
from apps.evidence.models import Evidence

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


def submit_case_to_storage(*, case, officer):
    """Case must be open"""
    if case.status != Case.Status.OPEN:
        raise ValueError("Only open cases can be submitted to the storage")
    
    """Case must have at least one evidence"""
    evidence_qs = case.case_evidence_items.all()
    if not evidence_qs.exists():
        raise ValueError("Case must have at least one evidence item.")
    
    # check every evidence has at least one file
    # for evidence in evidence_qs:
    #     if not evidence.evidence_files.exists():
    #         raise ValueError(f"Evidence must contain at least one evidence file.")
        
    """Optimization for the above code
        Each evidence must contain one file
    """
    evidence_without_files = evidence_qs.annotate(
        file_count=Count('evidence_files')
    ).filter(file_count=0)

    if evidence_without_files.exists():
        raise ValueError("All evidence items must have at least one file.")
    
    with transaction.atomic():
        case.status = Case.Status.SUBMITTED_TO_STORAGE
        case.save()

        AuditLog.objects.create(
            actor = officer,
            action = AuditLog.Action.CASE_SUBMITTED_TO_STORAGE,
            entity_type = "Case",
            entity_id = str(case.pk)
        )


def acknowledge_case(*,case,storage_clerk):
    if case.status != Case.Status.SUBMITTED_TO_STORAGE:
        raise ValueError("Already in storage.")
    
    with transaction.atomic():
        case.status = Case.Status.IN_STORAGE
        case.save()

        case.case_evidence_items.all().update(status=Evidence.Status.IN_STORAGE)

        AuditLog.objects.create(
            actor = storage_clerk,
            action = AuditLog.Action.CASE_IN_STORAGE,
            entity_type = "Case",
            entity_id = str(case.pk)
        )
