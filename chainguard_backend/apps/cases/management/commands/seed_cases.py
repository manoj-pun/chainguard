from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.cases.models import Case

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.filter(role="OFFICER").first()
        
        if not user:
            self.stdout.write(self.style.ERROR("No officer found"))
            return

        cases = [
            {
                "title": "Cyber Fraud - TechCorp Data Breach",
                "description": "Hackers stole customer credit card data from TechCorp's database. Occurred Jan 15, 2026. Need to trace attack source."
            },
            {
                "title": "Multi-Vehicle Accident - Main & 5th",
                "description": "Three-car collision at Main & 5th on Feb 1, 2026. Two injured. Review CCTV footage to determine liability."
            },
            {
                "title": "Domestic Violence - Highland Apartments",
                "description": "Physical altercation reported at Unit 304 on Feb 5, 2026. Victim has injuries. Interview witnesses and collect evidence."
            },
            {
                "title": "Jewelry Store Burglary - Oak Street",
                "description": "$250K in jewelry stolen from Smith & Sons on Feb 10, 2026. Entry via rear window. Security footage available."
            },
            {
                "title": "Hit and Run - Riverside Park",
                "description": "Pedestrian struck by dark sedan at Riverside Park on Feb 12, 2026. Driver fled the scene. Seeking witnesses."
            },
            {
                "title": "Drug Possession - Eastside Warehouse",
                "description": "Suspected drug trafficking operation at vacant warehouse. Methamphetamine and cash seized on Feb 14, 2026."
            },
            {
                "title": "Identity Theft Ring - University Area",
                "description": "Multiple students reported stolen identities. Suspects using fake IDs to open bank accounts. Undercover operation needed."
            },
            {
                "title": "Arson - Abandoned Factory",
                "description": "Suspicious fire at old textile factory on Feb 18, 2026. Multiple ignition points found. Investigate for insurance fraud."
            },
            {
                "title": "Cyber Fraud - TechCorp Data Breach",
                "description": "Hackers stole customer credit card data from TechCorp's database. Occurred Jan 15, 2026. Need to trace attack source."
            },
            {
                "title": "Multi-Vehicle Accident - Main & 5th",
                "description": "Three-car collision at Main & 5th on Feb 1, 2026. Two injured. Review CCTV footage to determine liability."
            },
            {
                "title": "Domestic Violence - Highland Apartments",
                "description": "Physical altercation reported at Unit 304 on Feb 5, 2026. Victim has injuries. Interview witnesses and collect evidence."
            },
            {
                "title": "Jewelry Store Burglary - Oak Street",
                "description": "$250K in jewelry stolen from Smith & Sons on Feb 10, 2026. Entry via rear window. Security footage available."
            },
            {
                "title": "Hit and Run - Riverside Park",
                "description": "Pedestrian struck by dark sedan at Riverside Park on Feb 12, 2026. Driver fled the scene. Seeking witnesses."
            },
            {
                "title": "Drug Possession - Eastside Warehouse",
                "description": "Suspected drug trafficking operation at vacant warehouse. Methamphetamine and cash seized on Feb 14, 2026."
            },
            {
                "title": "Identity Theft Ring - University Area",
                "description": "Multiple students reported stolen identities. Suspects using fake IDs to open bank accounts. Undercover operation needed."
            },
            {
                "title": "Arson - Abandoned Factory",
                "description": "Suspicious fire at old textile factory on Feb 18, 2026. Multiple ignition points found. Investigate for insurance fraud."
            },
            {
                "title": "Cyber Fraud - TechCorp Data Breach",
                "description": "Hackers stole customer credit card data from TechCorp's database. Occurred Jan 15, 2026. Need to trace attack source."
            },
            {
                "title": "Multi-Vehicle Accident - Main & 5th",
                "description": "Three-car collision at Main & 5th on Feb 1, 2026. Two injured. Review CCTV footage to determine liability."
            },
            {
                "title": "Domestic Violence - Highland Apartments",
                "description": "Physical altercation reported at Unit 304 on Feb 5, 2026. Victim has injuries. Interview witnesses and collect evidence."
            },
            {
                "title": "Jewelry Store Burglary - Oak Street",
                "description": "$250K in jewelry stolen from Smith & Sons on Feb 10, 2026. Entry via rear window. Security footage available."
            },
            {
                "title": "Hit and Run - Riverside Park",
                "description": "Pedestrian struck by dark sedan at Riverside Park on Feb 12, 2026. Driver fled the scene. Seeking witnesses."
            },
            {
                "title": "Drug Possession - Eastside Warehouse",
                "description": "Suspected drug trafficking operation at vacant warehouse. Methamphetamine and cash seized on Feb 14, 2026."
            },
            {
                "title": "Identity Theft Ring - University Area",
                "description": "Multiple students reported stolen identities. Suspects using fake IDs to open bank accounts. Undercover operation needed."
            },
            {
                "title": "Arson - Abandoned Factory",
                "description": "Suspicious fire at old textile factory on Feb 18, 2026. Multiple ignition points found. Investigate for insurance fraud."
            }
        ]

        for c in cases:
            Case.objects.create(officer=user, **c)