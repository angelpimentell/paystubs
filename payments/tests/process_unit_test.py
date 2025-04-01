from rest_framework.test import APITestCase
from unittest.mock import patch
from datetime import datetime

class ProcessUnitTest(APITestCase):
    def setUp(self):
        self.url = "/process?country=do&credentials=admin+admin&company=default"

    @patch("payments.views.process_view.datetime")
    def test_process_with_valid_data(self, mock_datetime):
        # Arrange
        mock_datetime.now.return_value = datetime(2024, 4, 1, 12, 0, 0)
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@example.com,Developer,1,2,3,4,5,6,7,2025-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b'[{"email":"angelpimentelcontact@example.com","datetime":"2024-04-01T12:00:00"}]',
            response.content,
        )

    @patch("payments.views.process_view.datetime")
    def test_process_with_invalid_data(self, mock_datetime):
        # Arrange
        mock_datetime.now.return_value = datetime(2024, 4, 1, 12, 0, 0)
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@example.com,Developer,AAAAA,2,EEE3,4,5,6,7,20121225-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b'[{"email":"angelpimentelcontact@example.com","datetime":null,"message":"Wrong values from CSV."}]',
            response.content,
        )

    def test_process_with_invalid_credentials(self):
        # Arrange
        self.url = "/process?country=do&credentials=wronguser+admin&company=default"
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@example.com,Developer,1,2,3,4,5,6,7,2025-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 401)

    @patch("payments.views.process_view.datetime")
    def test_process_with_invalid_country_and_company(self, mock_datetime):
        # Arrange
        mock_datetime.now.return_value = datetime(2024, 4, 1, 12, 0, 0)
        self.url = "/process?country=wrongcontry&credentials=admin+admin&company=wrongdefault"
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@example.com,Developer,1,2,3,4,5,6,7,2025-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b'[{"email":"angelpimentelcontact@example.com","datetime":"2024-04-01T12:00:00"}]',
            response.content,
        )

