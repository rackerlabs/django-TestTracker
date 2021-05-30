#!/bin/sh
# Run available unittests with a setup for CI/CD:
# - Fail if migrations are not created
# - Exit container after running tests to allow exit code to propagate as test result
# set -x
# set -e
# set -v

cd /app
# Unset the database URL so that we can force the DD_TEST_DATABASE_NAME (see django "DATABASES" configuration in settings.dist.py)
unset DD_DATABASE_URL

# TARGET_SETTINGS_FILE=dojo/settings/settings.py
# if [ ! -f ${TARGET_SETTINGS_FILE} ]; then
#   echo "Creating settings.py"
#   cp dojo/settings/settings.dist.py dojo/settings/settings.py
# fi

python3 manage.py spectacular --fail-on-warn || {
    cat <<-EOF

********************************************************************************

You made changes to the REAST API without applying the correct schema annotations

These schema annotations are needed to allow for the correct generation of
the OpenAPI (v3) schema's and documentation.

Review the warnings generated by drf-spectacular and see `dojo/api_v2/views.py`
and/or `dojo/api_v2/serializers.py`.

You can check for warnings locally by running

     python3 manage.py spectacular > /dev/null

This will output only warnings/errors, or nothing if everything is OK.

More info at: https://drf-spectacular.readthedocs.io/en/latest/customization.html

********************************************************************************

EOF
    exit 1
}

python3 manage.py makemigrations --no-input --check --dry-run --verbosity 3 || {
    cat <<-EOF

********************************************************************************

You made changes to the models without creating a DB migration for them.

**NEVER** change existing migrations, create a new one.

If you're not familiar with migrations in Django, please read the
great documentation thoroughly:
https://docs.djangoproject.com/en/1.11/topics/migrations/

********************************************************************************

EOF
    exit 1
}

python3 manage.py migrate

# --parallel fails on GitHub Actions
#python3 manage.py test dojo.unittests -v 3 --no-input --parallel

echo "Swagger Schema Tests - Broken"
echo "------------------------------------------------------------"
python3 manage.py test dojo.unittests -v 3 --no-input --tag broken && true

echo "Unit Tests"
echo "------------------------------------------------------------"
python3 manage.py test dojo.unittests -v 3 --no-input --exclude-tag broken
