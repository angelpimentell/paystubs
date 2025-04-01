from rest_framework.test import APITestCase


class ProcessUnitTest(APITestCase):
    def setUp(self):
        self.url = "/process?country=do&credentials=admin+admin&company=default"

    def test_process_with_valid_data(self):
        # Arrange
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@gmail.com,Developer,1,2,3,4,5,6,7,2025-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_process_with_invalid_data(self):
        # Arrange
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@gmail.com,Developer,AAAAA,2,EEE3,4,5,6,7,20121225-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_process_with_invalid_credentials(self):
        # Arrange
        self.url = "/process?country=do&credentials=wronguser+admin&company=default"
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@gmail.com,Developer,1,2,3,4,5,6,7,2025-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_process_with_invalid_country_and_company(self):
        # Arrange
        self.url = "/process?country=wrongcontry&credentials=admin+admin&company=wrongdefault"
        csv_content = b"full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period"
        csv_content += b"\nAngel,angelpimentelcontact@gmail.com,Developer,1,2,3,4,5,6,7,2025-03-31"

        # Act
        response = self.client.post(
            self.url,
            data=csv_content,
            content_type="text/csv",
        )

        # Assert
        self.assertEqual(response.status_code, 200)
