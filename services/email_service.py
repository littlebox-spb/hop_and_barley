"""Сервис отправки электронных писем."""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from orders.models import Order

logger = logging.getLogger("orders.email")
User = get_user_model()


def send_order_created_emails(order: "Order") -> None:
    """
    Отправляет письма покупателю и администраторам.

    Письма НЕ отправляются, если email отсутствует.
    Ошибки SMTP НЕ ломают создание заказа.
    """
    from_email = settings.DEFAULT_FROM_EMAIL or "webmaster@localhost"

    # ==========================================================
    # 🧑‍💻 ПОКУПАТЕЛЬ
    # ==========================================================
    customer_email = getattr(order.user, "email", None)

    if customer_email:
        try:
            send_mail(
                subject=f"Ваш заказ №{order.id} принят",
                message=render_to_string(
                    "emails/order_created_customer.txt",
                    {"order": order},
                ),
                from_email=from_email,
                recipient_list=[customer_email],
            )
        except Exception as exc:
            logger.error(
                "Customer email failed (order %s): %s",
                order.id,
                exc,
                exc_info=True,
            )
    else:
        logger.info(
            "Customer email skipped (order %s): user has no email",
            order.id,
        )

    # ==========================================================
    # 🛠 АДМИНИСТРАТОРЫ
    # ==========================================================
    admin_emails = list(
        User.objects.filter(is_staff=True, is_active=True)
        .exclude(email__isnull=True)
        .exclude(email="")
        .values_list("email", flat=True)
    )

    if admin_emails:
        try:
            send_mail(
                subject=f"Новый заказ №{order.id}",
                message=render_to_string(
                    "emails/order_created_admin.txt",
                    {"order": order},
                ),
                from_email=from_email,
                recipient_list=admin_emails,
            )
        except Exception as exc:
            logger.error(
                "Admin email failed (order %s): %s",
                order.id,
                exc,
                exc_info=True,
            )
    else:
        logger.info(
            "Admin email skipped (order %s): no admin emails found",
            order.id,
        )
