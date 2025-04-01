from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import csv
import io
import os
from django.shortcuts import render

import pdfkit
from datetime import datetime
from dotenv import load_dotenv
from paystubs.helpers import check_template_exists

load_dotenv()


class ProcessView(APIView):

    def post(self, request, format=None):
        credentials = request.GET.get('credentials', None)
        username = credentials.split(" ")[0]
        password = credentials.split(" ")[1]

        if os.getenv("DJANGO_USERNAME") != username or os.getenv("DJANGO_PASSWORD") != password:
            return HttpResponse(status=401)

        country = request.GET.get('country', 'do')
        company_name = request.GET.get('company', 'default')
        template_name = f"{company_name}_{country}.html"

        if not check_template_exists(template_name):
            template_name = "default_do.html"

        decoded_file = io.StringIO(request.body.decode('utf-8'))
        csv_reader = csv.DictReader(decoded_file)
        emails_sends = []

        for row in csv_reader:
            gross_salary = float(row['gross_salary'])
            gross_payment = float(row['gross_payment'])
            net_payment = float(row['net_payment'])

            social_discount_amount = float(row['social_discount_amount'])
            health_discount_amount = float(row['health_discount_amount'])
            taxes_discount_amount = float(row['taxes_discount_amount'])
            other_discount_amount = float(row['other_discount_amount'])

            total_discounts = (
                    social_discount_amount + health_discount_amount +
                    taxes_discount_amount + other_discount_amount
            )

            html_string = render(
                request,
                template_name,
                {
                    "period": row['period'],
                    "comprobante_de_pago": row.get('comprobante_de_pago', 'N/A'),
                    "title": row.get('title', ''),
                    "full_name": row['full_name'],

                    "gross_salary": "{:.2f}".format(gross_salary),
                    "gross_payment": "{:.2f}".format(gross_payment),
                    "net_payment": "{:.2f}".format(net_payment),

                    "social_discount_amount": "{:.2f}".format(social_discount_amount),
                    "health_discount_amount": "{:.2f}".format(health_discount_amount),
                    "taxes_discount_amount": "{:.2f}".format(taxes_discount_amount),
                    "other_discount_amount": "{:.2f}".format(other_discount_amount),
                    "total_discounts": "{:.2f}".format(total_discounts),
                }
            ).content.decode("utf-8")

            pdfkit.from_string(html_string, row['email'].replace(".", "_") + ".pdf")

            # ACTION: Send email

            emails_sends.append({
                'email': row['email'],
                'datetime': datetime.now()
            })

        return Response(emails_sends)
