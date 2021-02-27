from django.test import TestCase
from dojo.models import Finding, Test
from django.contrib.auth.models import User
from unittest import mock
from crum import impersonate
import datetime
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)


frozen_datetime = timezone.make_aware(datetime.datetime(2021, 1, 1, 2, 2, 2), timezone.get_default_timezone())


class TestUpdateFindingStatusSignal(TestCase):
    fixtures = ['dojo_testdata.json']

    def setUp(self):
        self.user_1 = User.objects.get(id='1')
        self.user_2 = User.objects.get(id='2')

    def get_mitigation_status_fields(self, finding):
        return finding.active, finding.verified, finding.false_p, finding.out_of_scope, finding.is_Mitigated, finding.mitigated, finding.mitigated_by

    @mock.patch('dojo.finding.helper.datetime')
    def test_new_finding(self, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test)
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (True, True, False, False, False, None, None)
            )

    @mock.patch('dojo.finding.helper.datetime')
    def test_mark_fresh_as_mitigated(self, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test, is_Mitigated=True, active=False)
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (False, True, False, False, True, frozen_datetime, self.user_1)
            )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=False)
    def test_mark_old_active_as_mitigated(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test, is_Mitigated=True, active=False)
            finding.save()
            finding.is_Mitigated = True
            finding.active = False
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (False, True, False, False, True, frozen_datetime, self.user_1)
            )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=True)
    def test_mark_old_active_as_mitigated_custom_edit(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        custom_mitigated = datetime.datetime.now()

        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test)
            finding.save()
            finding.is_Mitigated = True
            finding.active = False
            finding.mitigated = custom_mitigated
            finding.mitigated_by = self.user_2
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (False, True, False, False, True, custom_mitigated, self.user_2)
            )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=True)
    def test_update_old_mitigated_with_custom_edit(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        custom_mitigated = datetime.datetime.now()

        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test, is_Mitigated=True, active=False, mitigated=frozen_datetime, mitigated_by=self.user_1)
            finding.save()
            finding.is_Mitigated = True
            finding.active = False
            finding.mitigated = custom_mitigated
            finding.mitigated_by = self.user_2
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (False, True, False, False, True, custom_mitigated, self.user_2)
            )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=False)
    def test_update_old_mitigated_with_custom_edit_not_allowed(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        custom_mitigated = datetime.datetime.now()

        with self.assertRaises(PermissionError):
            with impersonate(self.user_1):
                test = Test.objects.last()
                logger.debug('creating finding')
                finding = Finding(test=test, is_Mitigated=True, active=False, mitigated=frozen_datetime, mitigated_by=self.user_1)
                finding.save(dedupe_option=False)
                finding.is_Mitigated = True
                finding.active = False
                finding.mitigated = custom_mitigated
                finding.mitigated_by = self.user_2
                logger.debug('saving updated finding')
                finding.save(dedupe_option=False)

                self.assertEqual(
                    self.get_mitigation_status_fields(finding),
                    (False, True, False, False, True, frozen_datetime, self.user_1)
                )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=False)
    def test_update_old_mitigated_with_missing_data(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        custom_mitigated = datetime.datetime.now()

        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test, is_Mitigated=True, active=False, mitigated=custom_mitigated, mitigated_by=self.user_2)
            finding.save()
            finding.is_Mitigated = True
            finding.active = False
            # trying to remove mitigated fields will trigger the signal to set them to now/current user
            finding.mitigated = None
            finding.mitigated_by = None
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (False, True, False, False, True, frozen_datetime, self.user_1)
            )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=False)
    def test_set_old_mitigated_as_active(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test, is_Mitigated=True, active=False, mitigated=frozen_datetime, mitigated_by=self.user_2)
            finding.save()
            finding.active = True
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                (True, True, False, False, False, None, None)
            )

    @mock.patch('dojo.finding.helper.datetime')
    @mock.patch('dojo.finding.helper.timezone')
    @mock.patch('dojo.finding.helper.can_edit_mitigated_data', return_value=False)
    def test_set_active_as_false_p(self, mock_can_edit, mock_tz, mock_dt):
        mock_dt.now.return_value = frozen_datetime
        mock_tz.now.return_value = frozen_datetime

        with impersonate(self.user_1):
            test = Test.objects.last()
            finding = Finding(test=test)
            finding.save()
            finding.false_p = True
            finding.save()

            self.assertEqual(
                self.get_mitigation_status_fields(finding),
                # TODO marking as false positive resets verified to False, possible bug / undesired behaviour?
                (False, False, True, False, True, frozen_datetime, self.user_1)
            )
