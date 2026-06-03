# Unmatched Wiki

Student Django project for an Unmatched-style board game wiki.

## Check it out!
[Unmatched Wiki project deploy to render](https://unmatched-wiki.onrender.com)

## Features

- Custom user model
- User profile with avatar and bio
- Login, signup, logout and password reset with django-allauth
- Referral invites for user/editor registration
- Wiki pages for game sets, characters, maps, sidekicks and cards
- Search and filtering
- Slug URLs
- Admin customization
- Ready wiki data fixture
- Cloudinary support for media files on deploy

## Run project

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Create superuser

```bash
.venv/bin/python manage.py createsuperuser
```

## Referral invites

Login as staff user and open:

```text
http://127.0.0.1:8000/users/invites/
```

Create invite with role `Editor`. The email is printed in the runserver console because local project uses console email backend.

The invited user must register with the same email. After signup the user gets editor role and staff access.

Editors can edit wiki information from the site detail pages and from Django admin.

## Tests

```bash
.venv/bin/python manage.py test
```

## Project data

The project has a fixture with official Unmatched sets, characters, cards and maps:

```bash
.venv/bin/python manage.py loaddata fixtures/wiki_initial_data.json
```

Only official released sets were used for the wiki data. If the project is published publicly, images and card text should be used carefully because they belong to their original rights holders.

## Render deploy

This project has Render files:

```text
build.sh
render.yaml
```

Render build command:

```bash
./build.sh
```

Render start command:

```bash
python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```

During deploy the project runs migrations, loads initial wiki data if the
database is empty, and creates a deploy superuser if superuser environment
variables are set.

## Render environment variables

The database is configured with `DATABASE_URL`.

The current data stores Cloudinary public ids for images. Use `CLOUDINARY_URL` on Render to display and upload media files.

On Render set one of these options:

```text
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Or:

```text
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

Also set:

```text
DEBUG=False
SECRET_KEY=your_secret_key
DJANGO_SUPERUSER_USERNAME=user
DJANGO_SUPERUSER_EMAIL=user@example.com
DJANGO_SUPERUSER_PASSWORD=your_admin_password
```

New images uploaded from admin or editor forms will go to Cloudinary automatically.

## Demo

![Website interface](demo.png)

