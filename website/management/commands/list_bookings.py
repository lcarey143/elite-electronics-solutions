from django.core.management.base import BaseCommand

from website.models import Booking


class Command(BaseCommand):
    help = "List bookings in the database (use on Railway to verify admin data)"

    def handle(self, *args, **options):
        count = Booking.objects.count()
        self.stdout.write(f"Total bookings: {count}")
        if count == 0:
            self.stdout.write(
                "No bookings yet. Submit a test booking on the LIVE site "
                "(not localhost), then check admin on the same URL."
            )
            return

        for booking in Booking.objects.all()[:50]:
            self.stdout.write(
                f"  {booking.reference} | {booking.full_name} | {booking.email} | "
                f"{booking.preferred_date} | {booking.status} | {booking.created_at:%Y-%m-%d %H:%M}"
            )
