#!/bin/sh
# Run available unittests with a setup for local dev:
# - Make migrations and apply any needed changes
# - Leave container up after running tests to allow debugging, rerunning tests, etc.
set -x
set -e
set -v

. /secret-file-loader.sh

cd /app
# Unset the database URL so that we can force the DD_TEST_DATABASE_NAME (see django "DATABASES" configuration in settings.dist.py)
unset DD_DATABASE_URL

# Unset the celery broker URL so that we can force the other DD_CELERY_BROKER settings
unset DD_CELERY_BROKER_URL

python3 manage.py makemigrations dojo
python3 manage.py migrate

# do the check with Django stack
python3 manage.py check

python3 manage.py spectacular --fail-on-warn > /dev/null || {
    cat <<-EOF

********************************************************************************

You made changes to the REST API without applying the correct schema annotations

These schema annotations are needed to allow for the correct generation of
the OpenAPI (v3) schema's and documentation.

Review the warnings generated by drf-spectacular and see "dojo/api_v2/views.py"
and/or "dojo/api_v2/serializers.py".

You can check for warnings locally by running

     python3 manage.py spectacular > /dev/null

This will output only warnings/errors, or nothing if everything is OK.

More info at: https://drf-spectacular.readthedocs.io/en/latest/customization.html

********************************************************************************

EOF
    python3 manage.py spectacular > /dev/null
}

echo "Unit Tests"
echo "------------------------------------------------------------"
# python3 manage.py test unittests -v 3 --keepdb --no-input
python3 manage.py test unittests.test_import_reimport.ImportReimportTestAPI.test_import_default_scan_date_parser_not_sets_date -v 3 --keepdb --no-input

# you can select a single file to "test" unit tests
# python3 manage.py test unittests.tools.test_npm_audit_scan_parser.TestNpmAuditParser --keepdb -v 3

# or even a single method
# python3 manage.py test unittests.tools.test_npm_audit_scan_parser.TestNpmAuditParser.test_npm_audit_parser_many_vuln_npm7 --keepdb -v 3

echo "End of tests. Leaving the container up"
tail -f /dev/null
