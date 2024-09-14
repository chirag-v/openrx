# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import MedicalRepresentative
from .serializers import MedicalRepresentativeInfoSerializer

class MedicalRepresentativeInfo(APIView):
    view_name = 'Get Medical Representative Info'
    def get(self, request):
        med_rep_id = request.query_params.get('med_rep_id')
        if med_rep_id is not None:
            try:
                med_rep = MedicalRepresentative.objects.get(id=med_rep_id)
                if med_rep.division:
                    company_name = med_rep.division.company.name
                    division_name = med_rep.division.name
                    division_id = med_rep.division.id
                else:
                    company_name = med_rep.company.name if med_rep.company else 'N/A'
                    division_name = 'This company has no division'
                    division_id = ''

                data = {
                    'company': company_name,
                    'division': division_name,
                    'division_id': division_id
                }
                serializer = MedicalRepresentativeInfoSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except MedicalRepresentative.DoesNotExist:
                return Response({'error': 'Medical Representative not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'med_rep_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)


