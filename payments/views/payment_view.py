from rest_framework.views import APIView
from rest_framework.response import Response
import csv
import io

class PaymentView(APIView):

    def post(self, request, format=None):
        country = request.GET.get('country', 'do')
        credentials = request.GET.get('credentials', None)
        company_name = request.GET.get('company', None)

        decoded_file = io.StringIO(request.body.decode('utf-8'))
        csv_reader = csv.DictReader(decoded_file)

        data_list = []
        for row in csv_reader:
            data_list.append(row)

        return Response({'test': 'post'})
