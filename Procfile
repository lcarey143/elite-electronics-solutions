web: python manage.py migrate && python manage.py seed_data && python manage.py ensure_admin && python manage.py collectstatic --noinput && gunicorn ees_project.wsgi --bind 0.0.0.0:$PORT
