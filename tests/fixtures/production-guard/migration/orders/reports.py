from django.db.models import Count

from .models import Order


def orders_by_region() -> dict[str, int]:
    """Regional breakdown for the operations dashboard."""
    rows = Order.objects.values("region").annotate(total=Count("id"))
    return {row["region"]: row["total"] for row in rows}
