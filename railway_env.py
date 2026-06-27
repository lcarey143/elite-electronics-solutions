#!/usr/bin/env python
"""Print Railway environment variables to set in the dashboard."""
import secrets

print("""
Railway Environment Variables
=============================

Required:
  SECRET_KEY={secret_key}
  DEBUG=False
  DJANGO_SUPERUSER_USERNAME=admin
  DJANGO_SUPERUSER_EMAIL=lashardcarey@gmail.com
  DJANGO_SUPERUSER_PASSWORD=<choose-a-strong-password>

After generating your Railway domain (e.g. yourapp.up.railway.app):
  CSRF_TRUSTED_ORIGINS=https://yourapp.up.railway.app

Email (Gmail):
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_HOST_USER=lashardcarey@gmail.com
  EMAIL_HOST_PASSWORD=<gmail-app-password>
  EMAIL_USE_TLS=True
  DEFAULT_FROM_EMAIL=Elite Electronics Solutions <lashardcarey@gmail.com>

AI Assistant:
  OPENAI_API_KEY=<your-openai-key>
  OPENAI_MODEL=gpt-4o-mini

Notes:
  - Add a PostgreSQL plugin in Railway; DATABASE_URL is set automatically.
  - Deploy from GitHub repo: lcarey143/elite-electronics-solutions
  - Generate a public domain under Settings > Networking > Generate Domain
""".format(secret_key=secrets.token_urlsafe(50)))
