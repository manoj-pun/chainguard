from .models import Evidence, EvidenceFile
from apps.audits.models import AuditLog

"""use the below function if you know which data you need to take"""
# def create_evidence(*,officer,validated_data):
#     evidence = Evidence.objects.create(
#         officer = officer,
#         **validated_data
#     )

#     AuditLog.objects.create(
#         actor = officer,
#         action = AuditLog.Action.EVIDENCE_COLLECTED,
#         entity_type = "Evidence",
#         entity_id = str(evidence.pk)
#     )

#     return evidence


def create_evidence(*,officer,case, description):
    evidence = Evidence.objects.create(
        officer = officer,
        case = case,
        description = description
    )

    AuditLog.objects.create(
        actor = officer,
        action = AuditLog.Action.EVIDENCE_COLLECTED,
        entity_type = "Evidence",
        entity_id = str(evidence.pk)
    )

    return evidence



def create_evidence_file(*,officer,evidence,file,file_type):
    evidence_file = EvidenceFile.objects.create(
        evidence = evidence,
        file = file,
        file_type = file_type
    )

    AuditLog.objects.create(
        actor = officer,
        action = AuditLog.Action.EVIDENCE_FILE_UPLOADED,
        entity_type = "EvidenceFile",
        entity_id = str(evidence_file.pk)
    )
    return evidence_file
