from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.db.models import QuerySet
from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():

        order_kwargs = {"user": user}
        if date:
            parsed = parse_datetime(date)
            if parsed is None:
                raise ValueError("Invalid date format, use 'YYYY-MM-DD HH:MM'")
            order_kwargs["created_at"] = parsed

        order = Order.objects.create(**order_kwargs)

        for data in tickets:
            Ticket.objects.create(
                movie_session_id=data["movie_session"],
                order=order,
                row=data["row"],
                seat=data["seat"]
            )

    return order


def get_orders(username: str = None) -> (QuerySet[Order]):

    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
