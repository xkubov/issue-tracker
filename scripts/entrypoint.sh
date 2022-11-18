#!/bin/bash

set -x

# Migrate database.
/app/scripts/manage.py migrate

# Collect static files.
/app/scripts/manage.py collectstatic

if [ ! -z "$ADMIN_PASSWORD" ]; then
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', '$ADMIN_PASSWORD')" | python /app/scripts/manage.py shell
fi

# Run gunicorn server.
exec gunicorn -b 0.0.0.0:80 issue_tracker.wsgi
