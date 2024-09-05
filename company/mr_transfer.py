''' this is a function that can be used to transfer a medical
 representative from one division to another division

 1. The function takes in the id of the medical representative to be transferred, the id of the division the
 representative is leaving, and the id of the division the representative is joining.
 2. The function fetches the medical representative object using the id provided.
 3. The function fetches the division the representative is leaving using the id provided.
 4. The function updates the medical representative field of the division the representative is leaving to None or to
  another representative.
 5. If the id of the division the representative is joining is provided, the function fetches the division the
 representative is joining using the id provided.
 6. The function updates the medical representative field of the division the representative is joining to the medical
 representative object fetched in step 2.
 7. The function saves the changes made to the divisions.
 8. The function does not return any value.
 9. The function can be called to transfer a medical representative from one division to another by providing the
 necessary ids as arguments.
 10. The function can be used in a Django application that has models for Division and MedicalRepresentative as shown
 in the code snippet.
    Example usage: transfer_medical_representative(1, 2, 3)
    where 1 is the id of the medical representative, 2 is the id of the division the representative is leaving, and 3
    is the id of the division the representative is joining.

 '''

from .models import Division, MedicalRepresentative


def transfer_medical_representative(med_rep_id, leaving_division_id, joining_division_id=None):
    med_rep = MedicalRepresentative.objects.get(id=med_rep_id)

    # Update the division the representative is leaving
    leaving_division = Division.objects.get(id=leaving_division_id)
    leaving_division.medical_representative = None  # Or set to a new representative
    leaving_division.save()

    # If joining a new division
    if joining_division_id:
        joining_division = Division.objects.get(id=joining_division_id)
        joining_division.medical_representative = med_rep
        joining_division.save()
