from .models import Case

def create_case(*, officer, validated_data):
    case = Case.objects.create(
        officer = officer,
        **validated_data
    )

    return case