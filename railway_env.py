#!/usr/bin/env python
"""Print Railway environment variables for custom domain and email setup."""
import secrets

print("""
================================================================================
  EES WEBSITE — RAILWAY SETUP CHECKLIST
  Live site: https://eesbahamas.up.railway.app
================================================================================

ALREADY WORKING
  [x] Website live on Railway
  [x] Admin panel login
  [x] Database (PostgreSQL)

--------------------------------------------------------------------------------
1. CUSTOM DOMAIN (e.g. www.yourdomain.com)
--------------------------------------------------------------------------------

Step A — In Railway:
  • Open your web service → Settings → Networking
  • Click "Custom Domain" → enter your domain (e.g. eesbahamas.com)
  • Railway shows DNS records to add at your registrar

Step B — At your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.):
  • Add a CNAME record:
      Name/Host:  www   (or @ for root — use Railway's instructions)
      Value:      the target Railway gives you (often *.up.railway.app)

Step C — In Railway Variables, add:
  CUSTOM_DOMAIN=yourdomain.com,www.yourdomain.com
  CSRF_TRUSTED_ORIGINS=https://eesbahamas.up.railway.app,https://yourdomain.com,https://www.yourdomain.com

  (Keep the .up.railway.app URL in CSRF so both URLs work during transition)

Step D — Redeploy and wait for DNS (can take up to 48 hours, usually minutes)

--------------------------------------------------------------------------------
2. EMAIL — Booking notifications to lashardcarey@gmail.com
--------------------------------------------------------------------------------

Step A — Create a Gmail App Password:
  • Google Account → Security → 2-Step Verification (must be ON)
  • App passwords → Create → name it "EES Website"
  • Copy the 16-character password (no spaces)

Step B — In Railway Variables, set:
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_HOST_USER=lashardcarey@gmail.com
  EMAIL_HOST_PASSWORD=<your-16-char-app-password>
  EMAIL_USE_TLS=True
  DEFAULT_FROM_EMAIL=Elite Electronics Solutions <lashardcarey@gmail.com>

Step C — Redeploy, then submit a test booking on the site
  • You should receive email at lashardcarey@gmail.com
  • Customer gets a confirmation email too

--------------------------------------------------------------------------------
3. AI ASSISTANT (chat bubble on site)
--------------------------------------------------------------------------------

In Railway Variables:
  OPENAI_API_KEY=<your key from platform.openai.com>
  OPENAI_MODEL=gpt-4o-mini

--------------------------------------------------------------------------------
4. SECURITY (recommended)
--------------------------------------------------------------------------------

  SECRET_KEY={secret_key}
  DEBUG=False

================================================================================
""".format(secret_key=secrets.token_urlsafe(50)))
