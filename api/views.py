# api/views.py
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.models import MedicalRepresentative
from item.models import Item
from .serializers import MedicalRepresentativeInfoSerializer, ItemSerializer
from gst.models import StateCode


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


class GetStateName(APIView):
    view_name = 'Get State Name'
    def get(self, request):
        code = request.query_params.get('code')
        if code:
            state = StateCode.objects.filter(code=code).first()
            if state:
                return Response({'stateName': state.name})
            else:
                return Response({'error': 'State not found'}, status=404)
        return Response({'error': 'Code parameter is required'}, status=400)


# Pagination class for API
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Determine if there is a next or previous page
        has_next = self.page.has_next() if self.page else False
        has_previous = self.page.has_previous() if self.page else False

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count if self.page else 0,
            'per_page': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages if self.page else 0,
            'current_page': self.page.number if self.page else 1,
            'page_size': len(data),  # Number of items on the current page
            'has_next': has_next,
            'has_previous': has_previous,
            'start_index': self.page.start_index() if self.page else 0,
            'end_index': self.page.end_index() if self.page else 0,
            'results': data
        })


class GetItems(APIView):
    """
    Versatile API view to fetch and filter items.
    Supports search, filtering, sorting, and pagination.
    """
    view_name = 'Get Items'
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        try:
            # Initial queryset
            items = Item.objects.all()

            # Apply search filter if a query is provided
            search_query = request.query_params.get('q', None)
            if search_query:
                items = items.filter(
                    Q(name__icontains=search_query) |
                    Q(use__icontains=search_query) |
                    Q(batch_number__icontains=search_query) |
                    Q(sku__icontains=search_query)
                )

            # Apply filtering by various fields
            item_type = request.query_params.get('item_type', None)
            if item_type:
                items = items.filter(item_type=item_type)

            min_price = request.query_params.get('min_price', None)
            if min_price:
                try:
                    min_price = float(min_price)
                    items = items.filter(mrp__gte=min_price)
                except ValueError:
                    return Response({"error": "Invalid minimum price value."}, status=HTTP_400_BAD_REQUEST)

            max_price = request.query_params.get('max_price', None)
            if max_price:
                try:
                    max_price = float(max_price)
                    items = items.filter(mrp__lte=max_price)
                except ValueError:
                    return Response({"error": "Invalid maximum price value."}, status=HTTP_400_BAD_REQUEST)

            company_id = request.query_params.get('company_id', None)
            if company_id:
                items = items.filter(company_id=company_id)

            division_id = request.query_params.get('division_id', None)
            if division_id:
                items = items.filter(division_id=division_id)

            current_status = request.query_params.get('current_status', None)
            if current_status:
                items = items.filter(current_status=current_status)

            prescription_required = request.query_params.get('prescription_required', None)
            if prescription_required is not None:
                items = items.filter(prescription_required=(prescription_required.lower() == 'true'))

            # Apply sorting
            valid_sort_fields = ['name', 'mrp', 'created_at', 'updated_at', 'weight', 'sku']  # Specify valid fields
            sort_by = request.query_params.get('sort_by', 'name')  # Default sorting by name
            if sort_by not in valid_sort_fields:
                return Response({"error": f"Invalid sort field: {sort_by}. Must be one of {valid_sort_fields}."},
                                status=HTTP_400_BAD_REQUEST)

            order = request.query_params.get('order', 'asc')  # Default order is ascending
            if order == 'desc':
                sort_by = '-' + sort_by
            elif order != 'asc':
                return Response({"error": "Invalid order. Must be 'asc' or 'desc'."},
                                status=HTTP_400_BAD_REQUEST)

            items = items.order_by(sort_by)

            # Paginate the queryset
            paginator = self.pagination_class()
            paginated_items = paginator.paginate_queryset(items, request, view=self)
            serializer = self.serializer_class(paginated_items, many=True)

            # Return paginated response
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            # Handle exceptions gracefully
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
