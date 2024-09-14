# company/serializers.py
from rest_framework import serializers

class MedicalRepresentativeInfoSerializer(serializers.Serializer):
    company = serializers.CharField()
    division = serializers.CharField()
    division_id = serializers.CharField(allow_blank=True)