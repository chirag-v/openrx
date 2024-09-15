# company/serializers.py
from rest_framework import serializers

from company.models import Company, Division
from item.models import Item


class MedicalRepresentativeInfoSerializer(serializers.Serializer):
    company = serializers.CharField()
    division = serializers.CharField()
    division_id = serializers.CharField(allow_blank=True)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']  # Include other fields as needed

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name']  # Include other fields as needed

class ItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    division = DivisionSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
