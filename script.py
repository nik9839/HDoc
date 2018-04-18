import django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HDoc.settings")
django.setup()


if __name__ == "__main__":
    from Content.views import refresh_current_booking_no

    refresh_current_booking_no()
