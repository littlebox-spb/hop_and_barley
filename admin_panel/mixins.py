"""Mixins for admin panel."""

from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin


class StaffRequiredMixin(UserPassesTestMixin):
    """Check if user is staff."""

    def test_func(self: Any) -> Any:
        """Check if user is staff."""
        return self.request.user.is_authenticated and self.request.user.is_staff
