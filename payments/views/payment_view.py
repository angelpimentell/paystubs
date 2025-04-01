from rest_framework.views import APIView
from rest_framework.response import Response
import csv
import io
from django.shortcuts import render

import pdfkit
from datetime import datetime


class PaymentView(APIView):

    def post(self, request, format=None):
        country = request.GET.get('country', 'do')
        credentials = request.GET.get('credentials', None)
        company_name = request.GET.get('company', 'default')

        decoded_file = io.StringIO(request.body.decode('utf-8'))
        csv_reader = csv.DictReader(decoded_file)
        emails_sends = []
        template_name = f"{company_name}_{country}.html"

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
