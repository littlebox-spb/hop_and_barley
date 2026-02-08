from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from orders.models import Order
from services.email_service import send_order_created_emails

User = get_user_model()

# Тесты Email


class OrderEmailServiceTests(TestCase):
    def setUp(self):
        self.user_with_email = User.objects.create_user(
            username="user1",
            email="user@example.com",
            password="123",
        )

        self.user_without_email = User.objects.create_user(
            username="user2",
            password="123",
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="123",
            is_staff=True,
        )

    def test_emails_sent_when_addresses_exist(self):
        order = Order.objects.create(
            user=self.user_with_email,
            total_price=100,
        )

        send_order_created_emails(order)

        self.assertEqual(len(mail.outbox), 2)

        recipients = sorted([mail.outbox[0].to[0], mail.outbox[1].to[0]])
        self.assertEqual(
            recipients,
            ["admin@example.com", "user@example.com"],
        )

    def test_customer_email_skipped_if_missing(self):
        order = Order.objects.create(
            user=self.user_without_email,
            total_price=100,
        )

        send_order_created_emails(order)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["admin@example.com"])

    def test_admin_email_skipped_if_no_admins(self):
        User.objects.filter(is_staff=True).delete()

        order = Order.objects.create(
            user=self.user_with_email,
            total_price=100,
        )

        send_order_created_emails(order)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@example.com"])
