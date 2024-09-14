# company/mr_transfer.py
import logging
from .models import MedicalRepresentative, Division, Company

logger = logging.getLogger(__name__)

def transfer_medical_representative(med_rep_id, leaving_division_id=None, joining_division_id=None, joining_company_id=None):
    try:
        med_rep = MedicalRepresentative.objects.get(id=med_rep_id)

        if leaving_division_id:
            leaving_division = Division.objects.get(id=leaving_division_id)
            if med_rep.division != leaving_division:
                raise ValueError("The Medical Representative does not belong to the specified leaving division.")
        else:
            if med_rep.division:
                raise ValueError("The Medical Representative belongs to a division, but no leaving division was specified.")

        if joining_division_id and joining_division_id != 'Selected company has no division':
            joining_division = Division.objects.get(id=joining_division_id)
            med_rep.division = joining_division
            med_rep.company = joining_division.company
        elif joining_company_id:
            joining_company = Company.objects.get(id=joining_company_id)
            med_rep.company = joining_company
            med_rep.division = None
        else:
            raise ValueError("Either joining_division_id or joining_company_id must be provided.")

        med_rep.save()
        return True
    except MedicalRepresentative.DoesNotExist:
        logger.error(f"MedicalRepresentative with id {med_rep_id} does not exist.")
        return False
    except Division.DoesNotExist:
        logger.error(f"Division with id {leaving_division_id} or {joining_division_id} does not exist.")
        return False
    except Company.DoesNotExist:
        logger.error(f"Company with id {joining_company_id} does not exist.")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False