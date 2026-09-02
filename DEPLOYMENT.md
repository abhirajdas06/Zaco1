# Deployment Guide — Ubuntu 22.04

Deploys the Zaco Django site with **Gunicorn** (app server) + **WhiteNoise**
(static files, served straight out of Gunicorn — no separate static-file
server needed) behind **nginx** (TLS termination, reverse proxy, media
files).

**Target environment**

| | |
|---|---|
| OS | Ubuntu Linux 22.04 LTS |
| Timezone | Asia/Kolkata (IST, UTC+5:30) |
| Server login user | `abc` |
| Process owner / group | `abc` / `www-data` |
| App directory | `/home/abc/zaco` |

---

## 0. One-time: rotate leaked secrets

Before going further: `secret_key.txt` and a Gmail SMTP app password were
previously **hardcoded and committed to git** in this repo's history. Even
though the code no longer reads secrets that way, those old values are
still recoverable from git history, so treat them as compromised:

1. Generate a brand new `DJANGO_SECRET_KEY`:
   ```bash
   python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. In your Google Account, revoke the old Gmail **App Password** and create
   a new one for `EMAIL_HOST_PASSWORD` (myaccount.google.com → Security →
   App Passwords). Never reuse the old one.

Both new values go into the server's `.env` file (step 5), never into the
repo.

---

## 1. Base server setup

```bash
sudo apt update && sudo apt upgrade -y

# Timezone
sudo timedatectl set-timezone Asia/Kolkata
timedatectl   # verify

# Core packages
sudo apt install -y python3 python3-venv python3-pip python3-dev \
    build-essential libjpeg-dev zlib1g-dev git nginx ufw
```

`libjpeg-dev`/`zlib1g-dev` are needed for Pillow's image handling (used by
CKEditor/Summernote uploads).

Create the `abc` user if it doesn't already exist, and make sure it's
around for the app to run as:

```bash
sudo adduser abc          # skip if the user already exists
sudo usermod -aG sudo abc # optional, only if abc needs sudo
```

Firewall:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 2. Get the code

As the `abc` user:

```bash
sudo -iu abc
git clone https://github.com/Owais0246/Zaco.git /home/abc/zaco
cd /home/abc/zaco/website
```

(If you deploy from a zip/rsync instead of git, just place the contents at
the same path.)

---

## 3. Python environment

```bash
cd /home/abc/zaco
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r website/requirement.txt
```

---

## 4. Configure environment variables

```bash
cd /home/abc/zaco/website
cp .env.example .env
nano .env
```

Fill in at minimum:

```
DJANGO_SECRET_KEY=<the value generated in step 0>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=zacoinfotech.com,www.zacoinfotech.com
DJANGO_SECURE_SSL_REDIRECT=False   # flip to True after step 8 (HTTPS)
EMAIL_HOST_USER=your-address@gmail.com
EMAIL_HOST_PASSWORD=<the new app password from step 0>
```

`.env` is gitignored — it must only ever exist on the server, never in the
repo.

---

## 5. Database, static files, superuser

Still as `abc`, with the venv active:

```bash
cd /home/abc/zaco/website
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

`collectstatic` writes hashed, compressed copies of every file under
`static/` into `staticfiles/` (per `STATIC_ROOT`) using WhiteNoise's
`CompressedManifestStaticFilesStorage`. Gunicorn/WhiteNoise serves directly
from there — run this command again after every deploy that changes static
assets.

Fix ownership so nginx (running as `www-data`) can read uploaded media,
while `abc` keeps write access:

```bash
sudo mkdir -p /home/abc/zaco/website/media
sudo chown -R abc:www-data /home/abc/zaco/website/media
sudo chmod -R 2775 /home/abc/zaco/website/media   # setgid so new uploads inherit www-data
```

---

## 6. Gunicorn as a systemd service

Create `/etc/systemd/system/gunicorn-zaco.service`:

```ini
[Unit]
Description=Gunicorn daemon for the Zaco Django site
After=network.target

[Service]
User=abc
Group=www-data
WorkingDirectory=/home/abc/zaco/website
RuntimeDirectory=gunicorn-zaco
ExecStart=/home/abc/zaco/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn-zaco/zaco.sock \
          website.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`RuntimeDirectory=gunicorn-zaco` makes systemd create `/run/gunicorn-zaco/`
(owned by `abc:www-data`) on every start, so the socket directory survives
reboots without manual `tmpfiles.d` setup. 3 workers is a reasonable start
for a small VPS — a common rule of thumb is `(2 × CPU cores) + 1`.

`website.wsgi:application` already picks up `.env` via `python-dotenv`
inside `settings.py`, so no `EnvironmentFile=` directive is needed.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-zaco
sudo systemctl status gunicorn-zaco
```

---

## 7. nginx reverse proxy

Create `/etc/nginx/sites-available/zaco`:

```nginx
server {
    listen 80;
    server_name zacoinfotech.com www.zacoinfotech.com;

    client_max_body_size 20M;

    # User-uploaded files (CKEditor/Summernote images etc.) — served
    # directly by nginx for speed. Static assets (CSS/JS/theme images) are
    # intentionally NOT listed here: WhiteNoise serves those through
    # Gunicorn instead.
    location /media/ {
        alias /home/abc/zaco/website/media/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn-zaco/zaco.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/zaco /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

At this point the site should be reachable over plain HTTP on your domain.

---

## 8. HTTPS with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d zacoinfotech.com -d www.zacoinfotech.com
```

Certbot rewrites the nginx server block to add a 443 listener and an
HTTP→HTTPS redirect, and installs a systemd timer for auto-renewal
(`sudo systemctl status certbot.timer`).

Then flip the app-level redirect back on: edit `.env` and set

```
DJANGO_SECURE_SSL_REDIRECT=True
```

restart Gunicorn:

```bash
sudo systemctl restart gunicorn-zaco
```

With `DEBUG=False`, `settings.py` also turns on `SESSION_COOKIE_SECURE`,
`CSRF_COOKIE_SECURE`, and HSTS automatically at this point.

---

## 9. Deploying updates

```bash
sudo -iu abc
cd /home/abc/zaco
git pull
source venv/bin/activate
pip install -r website/requirement.txt
cd website
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-zaco
```

---

## 10. Useful commands

```bash
# App logs (stdout/stderr of gunicorn)
sudo journalctl -u gunicorn-zaco -f

# nginx logs
sudo tail -f /var/log/nginx/error.log /var/log/nginx/access.log

# Restart everything after a config change
sudo systemctl restart gunicorn-zaco
sudo systemctl reload nginx
```

## 11. Backups

The database is SQLite at `website/db.sqlite3`. Back it up regularly, e.g.
a nightly cron job as `abc`:

```bash
mkdir -p /home/abc/backups
cp /home/abc/zaco/website/db.sqlite3 /home/abc/backups/db-$(date +\%F).sqlite3
```

Also back up `website/media/` (user uploads) — it's not in git.

---

## Troubleshooting

- **502 Bad Gateway**: Gunicorn isn't running or the socket path is wrong.
  Check `sudo systemctl status gunicorn-zaco` and confirm
  `/run/gunicorn-zaco/zaco.sock` exists.
- **Static files 404 / unstyled site**: run `collectstatic` again and
  confirm `DEBUG=False`/`True` matches what you expect — WhiteNoise reads
  from `STATIC_ROOT` (`staticfiles/`), not `static/` directly.
- **CSS/JS changed but browser shows old version**: expected —
  `CompressedManifestStaticFilesStorage` gives every file a
  content-hashed filename, so browsers cache old versions forever but the
  HTML always references the new hash after `collectstatic`.
- **500 error, nothing in nginx log**: check
  `sudo journalctl -u gunicorn-zaco -n 100` for the Django traceback.
- **`RuntimeError: DJANGO_SECRET_KEY is not set`**: `.env` is missing or
  not being found — confirm it's at `/home/abc/zaco/website/.env`.
