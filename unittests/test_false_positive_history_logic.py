from .dojo_test_case import DojoTestCase
from dojo.models import Finding, User, Product, Endpoint, Endpoint_Status, Test, Engagement
from dojo.models import System_Settings
from crum import impersonate
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
deduplicationLogger = logging.getLogger("dojo.specific-loggers.deduplication")

# Test data summary. All engagements have deduplication_on_engagement set to true.
#
# product 1: Python How-to
#       engagement 2: April monthly engagement (dedupe_inside: True)
#               test 13: ZAP Scan (algo=hash_code, dynamic=True)
#               no findings
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#
# product 2: Security How-to
#       engagement 1: 1st Quarter Engagement (dedupe_inside: True)
#               test 3: ZAP Scan (algo=hash_code, dynamic=True)
#               findings:
#                       2   : "High Impact Test Fin": High : act: True : ver: True : mit: False: dup: False: dup_id: None: hash_code: 5d368a051fdec959e08315a32ef633ba5711bed6e8e75319ddee2cab4d4608c7: eps: 0: notes: []: uid: None
#                       3   : "High Impact Test Fin": High : act: True : ver: True : mit: False: dup: True : dup_id: 2   : hash_code: 5d368a051fdec959e08315a32ef633ba5711bed6e8e75319ddee2cab4d4608c7: eps: 0: notes: []: uid: None
#                       4   : "High Impact Test Fin": High : act: True : ver: True : mit: False: dup: True : dup_id: 2   : hash_code: 5d368a051fdec959e08315a32ef633ba5711bed6e8e75319ddee2cab4d4608c7: eps: 0: notes: []: uid: None
#                       5   : "High Impact Test Fin": High : act: True : ver: True : mit: False: dup: True : dup_id: 2   : hash_code: 5d368a051fdec959e08315a32ef633ba5711bed6e8e75319ddee2cab4d4608c7: eps: 0: notes: []: uid: None
#                       6   : "High Impact Test Fin": High : act: True : ver: True : mit: False: dup: True : dup_id: 2   : hash_code: 5d368a051fdec959e08315a32ef633ba5711bed6e8e75319ddee2cab4d4608c7: eps: 0: notes: []: uid: None
#                       7   : "DUMMY FINDING       ": High : act: False: ver: False: mit: False: dup: False: dup_id: None: hash_code: c89d25e445b088ba339908f68e15e3177b78d22f3039d1bfea51c4be251bf4e0: eps: 0: notes: [1]: uid: None
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#               test 14: ZAP Scan (algo=hash_code, dynamic=True)
#               no findings
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#       engagement 4: April monthly engagement (dedupe_inside: True)
#               test 4: ZAP Scan (algo=hash_code, dynamic=True)
#               no findings
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#       engagement 5: April monthly engagement (dedupe_inside: True)
#               test 55: Checkmarx Scan detailed (algo=unique_id_from_tool, dynamic=False)
#               findings:
#                       124 : "Low Impact Test Find": Low  : act: True : ver: True : mit: False: dup: False: dup_id: None: hash_code: 9aca00affd340c4da02c934e7e3106a45c6ad0911da479daae421b3b28a2c1aa: eps: 0: notes: []: uid: 12345
#                       125 : "Low Impact Test Find": Low  : act: True : ver: True : mit: False: dup: True : dup_id: None: hash_code: 9aca00affd340c4da02c934e7e3106a45c6ad0911da479daae421b3b28a2c1aa: eps: 0: notes: []: uid: 12345
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#               test 66: Checkmarx Scan detailed (algo=unique_id_from_tool, dynamic=False)
#               no findings
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#               test 77: Veracode Scan (algo=unique_id_from_tool_or_hash_code, dynamic=False)
#               findings:
#                       224 : "UID Impact Test Find": Low  : act: True : ver: True : mit: False: dup: False: dup_id: None: hash_code: 6f8d0bf970c14175e597843f4679769a4775742549d90f902ff803de9244c7e1: eps: 0: notes: []: uid: 6789
#                       225 : "UID Impact Test Find": Low  : act: True : ver: True : mit: False: dup: True : dup_id: 224 : hash_code: 6f8d0bf970c14175e597843f4679769a4775742549d90f902ff803de9244c7e1: eps: 0: notes: []: uid: 6789
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#               test 88: Veracode Scan (algo=unique_id_from_tool_or_hash_code, dynamic=False)
#               no findings
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#       engagement 6: April monthly engagement (dedupe_inside: True)
#       engagement 3: weekly engagement (dedupe_inside: True)
#               test 33: Xanitizer Scan Findings Import (algo=legacy, dynamic=False)
#               findings:
#                       22  : "Low Impact Test Find": Low  : act: True : ver: True : mit: False: dup: False: dup_id: None: hash_code: 9aca00affd340c4da02c934e7e3106a45c6ad0911da479daae421b3b28a2c1aa: eps: 0: notes: []: uid: None
#                       23  : "Low Impact Test Find": Low  : act: True : ver: True : mit: False: dup: True : dup_id: 22  : hash_code: 9aca00affd340c4da02c934e7e3106a45c6ad0911da479daae421b3b28a2c1aa: eps: 0: notes: []: uid: None
#                       24  : "Low Impact Test Find": Low  : act: True : ver: True : mit: False: dup: True : dup_id: 22  : hash_code: 9aca00affd340c4da02c934e7e3106a45c6ad0911da479daae421b3b28a2c1aa: eps: 0: notes: []: uid: None
#               endpoints
#                       2: ftp://localhost/
#                       1: http://127.0.0.1/endpoint/420/edit/
#                       3: ssh:127.0.1
#               endpoint statuses
#                       1: dojo.Endpoint.None dojo.Finding.None 1 2020-07-01 00:00:00+00:00 2020-07-01 17:45:39.791907+00:00 False None None False False False ftp://localhost/ High Impact Test Finding
#
# product 3: Security Podcast

class TestFalsePositiveHistoryLogic(DojoTestCase):
    fixtures = ['dojo_testdata.json']

    def run(self, result=None):
        testuser = User.objects.get(username='admin')
        testuser.usercontactinfo.block_execution = True
        testuser.save()

        # Unit tests are running without any user, which will result in actions like dedupe happening in the celery process
        # this doesn't work in unittests as unittests are using an in memory sqlite database and celery can't see the data
        # so we're running the test under the admin user context and set block_execution to True
        with impersonate(testuser):
            super().run(result)

    def setUp(self):
        logger.debug('disabling dedupe')
        self.disable_dedupe()
        logger.debug('enabling false positive history')
        self.enable_false_positive_history()
        self.log_summary()

    def tearDown(self):
        self.log_summary()


    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_same_test(self):
        # Make a copy of finding 2 and store it in the same test (to test retroactive replication)
        finding_created_before_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make another copy of finding 2 and store it in the same test
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.save()
        # Assert that both findings belongs to the same test and are marked as fp
        self.assert_finding(finding_created_before_mark, false_p=True, not_pk=2, test_id=3, hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=True, not_pk=2, test_id=3, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_same_test_dedupe_enabled(self):
        # Enable deduplication
        self.enable_dedupe()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 2 and store it in the same test
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.save()
        # Assert that finding belongs to the same test and is NOT marked as fp
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=2, test_id=3, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    # Finding 7 in Product 2, Engagement 1, Test 3 (has a different hash code)
    def test_fp_history_different_hash_code_same_test(self):
        # Make a copy of finding 7 and store it in the same test (to test retroactive replication)
        finding_created_before_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make another copy of finding 7 and store it in the same test
        finding_created_after_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_after_mark.save()
        # Assert that both findings belongs to the same test and are NOT marked as fp
        self.assert_finding(finding_created_before_mark, false_p=False, not_pk=7, test_id=3, not_hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=7, test_id=3, not_hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_same_engagement_different_test(self):
        # Make a copy of finding 2 and store it at Product 2, Engagement 1, Test 14 (to test retroactive replication)
        finding_created_before_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_before_mark.test = Test.objects.get(id=14)
        finding_created_before_mark.save()
        # Mark as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make another copy of finding 2 and store it at Product 2, Engagement 1, Test 14
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.test = Test.objects.get(id=14)
        finding_created_after_mark.save()
        # Assert that both findings belongs to the same engagement but in a different test and are marked as fp
        self.assert_finding(finding_created_before_mark, false_p=True, not_pk=2, engagement_id=1, not_test_id=3, hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=True, not_pk=2, engagement_id=1, not_test_id=3, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_same_engagement_different_test_dedupe_enabled(self):
        # Enable deduplication
        self.enable_dedupe()
        # Mark as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 2 and store it at Product 2, Engagement 1, Test 14
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.test = Test.objects.get(id=14)
        finding_created_after_mark.save()
        # Assert that finding belongs to the same engagement but in a different test and is NOT marked as fp
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=7, engagement_id=1, not_test_id=3, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    # Finding 7 in Product 2, Engagement 1, Test 3 (has a different hash code)
    def test_fp_history_different_hash_code_same_engagement_different_test(self):
        # Make a copy of finding 7 and store it at Product 2, Engagement 1, Test 14 (to test retroactive replication)
        finding_created_before_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_before_mark.test = Test.objects.get(id=14)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 7 and store it at Product 2, Engagement 1, Test 14
        finding_created_after_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_after_mark.test = Test.objects.get(id=14)
        finding_created_after_mark.save()
        # Assert that both findings belongs to the same engagement but in a different test and are NOT marked as fp
        self.assert_finding(finding_created_before_mark, false_p=False, not_pk=7, engagement_id=1, not_test_id=3, not_hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=7, engagement_id=1, not_test_id=3, not_hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_same_product_different_engagement(self):
        # Make a copy of finding 2 and store it at Product 2, Engagement 4, Test 4 (to test retroactive replication)
        finding_created_before_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_before_mark.test = Test.objects.get(id=4)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 2 and store it at Product 2, Engagement 4, Test 4
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.test = Test.objects.get(id=4)
        finding_created_after_mark.save()
        # Assert that both findings belongs to the same engagement but in a different test and are marked as fp
        self.assert_finding(finding_created_before_mark, false_p=True, not_pk=2, product_id=2, not_engagement_id=1, hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=True, not_pk=2, product_id=2, not_engagement_id=1, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_same_product_different_engagement_dedupe_enabled(self):
        # Enable deduplication
        self.enable_dedupe()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 2 and store it at Product 2, Engagement 4, Test 4
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.test = Test.objects.get(id=4)
        finding_created_after_mark.save()
        # Assert that finding belongs to the same engagement but in a different test and is NOT marked as fp
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=2, product_id=2, not_engagement_id=1, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    # Finding 7 in Product 2, Engagement 1, Test 3 (has a different hash code)
    def test_fp_history_different_hash_code_same_product_different_engagement(self):
        # Make a copy of finding 7 and store it at Product 2, Engagement 4, Test 4 (to test retroactive replication)
        finding_created_before_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_before_mark.test = Test.objects.get(id=4)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 7 and store it at Product 2, Engagement 4, Test 4
        finding_created_after_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_after_mark.test = Test.objects.get(id=4)
        finding_created_after_mark.save()
        # Assert that both findings belongs to the same engagement but in a different test and are NOT marked as fp
        self.assert_finding(finding_created_before_mark, false_p=False, not_pk=7, product_id=2, not_engagement_id=1, not_hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=7, product_id=2, not_engagement_id=1, not_hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_different_product(self):
        # Make a copy of finding 2 and store it at Product 1, Engagement 2, Test 13 (to test retroactive replication)
        finding_created_before_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_before_mark.test = Test.objects.get(id=13)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 2 and store it at Product 1, Engagement 2, Test 13
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.test = Test.objects.get(id=13)
        finding_created_after_mark.save()
        # Assert that both findings belongs to a different product and are NOT marked as fp
        self.assert_finding(finding_created_before_mark, false_p=False, not_pk=2, not_product_id=2, hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=2, not_product_id=2, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    def test_fp_history_equal_hash_code_different_product_dedupe_enabled(self):
        # Enable deduplication
        self.enable_dedupe()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make a copy of finding 2 and store it at Product 1, Engagement 2, Test 13
        finding_created_after_mark, finding_2 = self.copy_and_reset_finding(id=2)
        finding_created_after_mark.test = Test.objects.get(id=13)
        finding_created_after_mark.save()
        # Assert that finding belongs to a different product and is NOT marked as fp
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=2, not_product_id=2, hash_code=finding_2.hash_code)

    # Finding 2 in Product 2, Engagement 1, Test 3
    # Finding 7 in Product 2, Engagement 1, Test 3 (has a different hash code)
    def test_fp_history_different_hash_code_different_product(self):
        # Make a copy of finding 7 and store it at Product 1, Engagement 2, Test 13 (to test retroactive replication)
        finding_created_before_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_before_mark.test = Test.objects.get(id=13)
        finding_created_before_mark.save()
        # Mark finding 2 as fp
        finding_2 = Finding.objects.get(id=2)
        finding_2.false_p = True
        finding_2.save()
        # Make another copy of finding 7 and store it at Product 1, Engagement 2, Test 13
        finding_created_after_mark, finding_7 = self.copy_and_reset_finding(id=7)
        finding_created_after_mark.test = Test.objects.get(id=13)
        finding_created_after_mark.save()
        # Assert that both findings belongs to a different product and are NOT marked as fp
        self.assert_finding(finding_created_before_mark, false_p=False, not_pk=7, not_product_id=2, not_hash_code=finding_2.hash_code)
        self.assert_finding(finding_created_after_mark, false_p=False, not_pk=7, not_product_id=2, not_hash_code=finding_2.hash_code)


    # # utility methods

    def log_product(self, product):
        if isinstance(product, int):
            product = Product.objects.get(pk=product)

        logger.debug('product %i: %s', product.id, product.name)
        for eng in product.engagement_set.all():
            self.log_engagement(eng)
            for test in eng.test_set.all():
                self.log_test(test)

    def log_engagement(self, eng):
        if isinstance(eng, int):
            eng = Engagement.objects.get(pk=eng)

        logger.debug('\t' + 'engagement %i: %s (dedupe_inside: %s)', eng.id, eng.name, eng.deduplication_on_engagement)

    def log_test(self, test):
        if isinstance(test, int):
            test = Test.objects.get(pk=test)

        logger.debug('\t\t' + 'test %i: %s (algo=%s, dynamic=%s)', test.id, test, test.deduplication_algorithm, test.test_type.dynamic_tool)
        self.log_findings(test.finding_set.all())

    def log_all_products(self):
        for product in Product.objects.all():
            self.log_summary(product=product)

    def log_findings(self, findings):
        if not findings:
            logger.debug('\t\t' + 'no findings')
        else:
            logger.debug('\t\t' + 'findings:')
            for finding in findings:
                logger.debug('\t\t\t{:4.4}'.format(str(finding.id)) + ': "' + '{:20.20}'.format(finding.title) + '": ' + '{:5.5}'.format(finding.severity) + ': act: ' + '{:5.5}'.format(str(finding.active)) +
                        ': ver: ' + '{:5.5}'.format(str(finding.verified)) + ': mit: ' + '{:5.5}'.format(str(finding.is_mitigated)) +
                        ': dup: ' + '{:5.5}'.format(str(finding.duplicate)) + ': dup_id: ' +
                        ('{:4.4}'.format(str(finding.duplicate_finding.id)) if finding.duplicate_finding else 'None') + ': hash_code: ' + str(finding.hash_code) +
                        ': eps: ' + str(finding.endpoints.count()) + ": notes: " + str([n.id for n in finding.notes.all()]) +
                        ': uid: ' + '{:5.5}'.format(str(finding.unique_id_from_tool)) + (' fp' if finding.false_p else '')
                        )

        logger.debug('\t\tendpoints')
        for ep in Endpoint.objects.all():
            logger.debug('\t\t\t' + str(ep.id) + ': ' + str(ep))

        logger.debug('\t\t' + 'endpoint statuses')
        for eps in Endpoint_Status.objects.all():
            logger.debug('\t\t\t' + str(eps.id) + ': ' + str(eps))

    def log_summary(self, product=None, engagement=None, test=None):
        if product:
            self.log_product(product)

        if engagement:
            self.log_engagement(engagement)

        if test:
            self.log_test(test)

        if not product and not engagement and not test:
            self.log_all_products()

    def copy_and_reset_finding(self, id):
        org = Finding.objects.get(id=id)
        new = org
        new.pk = None
        new.duplicate = False
        new.duplicate_finding = None
        new.false_p = False
        new.active = True
        new.hash_code = None
        # return unsaved new finding and reloaded existing finding
        return new, Finding.objects.get(id=id)

    def copy_and_reset_test(self, id):
        org = Test.objects.get(id=id)
        new = org
        new.pk = None
        # return unsaved new test and reloaded existing test
        return new, Test.objects.get(id=id)

    def copy_and_reset_engagement(self, id):
        org = Engagement.objects.get(id=id)
        new = org
        new.pk = None
        # return unsaved new engagement and reloaded existing engagement
        return new, Engagement.objects.get(id=id)

    def copy_and_reset_product(self, id):
        org = Product.objects.get(id=id)
        new = org
        new.pk = None
        new.name = '%s (Copy %s)' % (org.name, datetime.now())
        # return unsaved new product and reloaded existing product
        return new, Product.objects.get(id=id)

    def assert_finding(
            self, finding, false_p, duplicate=None, not_pk=None, hash_code=None,
            not_hash_code=None, unique_id_from_tool=None, not_unique_id_from_tool=None,
            test_id=None, not_test_id=None, engagement_id=None, not_engagement_id=None,
            product_id=None, not_product_id=None
        ):
        # Ensure we're always asserting against the latest state
        finding = Finding.objects.get(id=finding.id)

        self.assertEqual(finding.false_p, false_p)

        if duplicate:
            self.assertEqual(finding.duplicate, duplicate)

        if not_pk:
            self.assertNotEqual(finding.pk, not_pk)

        if hash_code:
            self.assertEqual(finding.hash_code, hash_code)

        if not_hash_code:
            self.assertNotEqual(finding.hash_code, not_hash_code)

        if unique_id_from_tool:
            self.assertEqual(finding.unique_id_from_tool, unique_id_from_tool)

        if not_unique_id_from_tool:
            self.assertNotEqual(finding.unique_id_from_tool, not_unique_id_from_tool)

        if test_id:
            self.assertEqual(finding.test.id, test_id)

        if not_test_id:
            self.assertNotEqual(finding.test.id, not_test_id)

        if engagement_id:
            self.assertEqual(finding.test.engagement.id, engagement_id)

        if not_engagement_id:
            self.assertNotEqual(finding.test.engagement.id, not_engagement_id)

        if product_id:
            self.assertEqual(finding.test.engagement.product.id, product_id)

        if not_product_id:
            self.assertNotEqual(finding.test.engagement.product.id, not_product_id)

    def set_dedupe_inside_engagement(self, deduplication_on_engagement):
        for eng in Engagement.objects.all():
            logger.debug('setting deduplication_on_engagment to %s for %i', str(deduplication_on_engagement), eng.id)
            eng.deduplication_on_engagement = deduplication_on_engagement
            eng.save()

    def create_new_test_and_engagment_from_finding(self, finding):
        eng_new, eng = self.copy_and_reset_engagement(id=finding.test.engagement.id)
        eng_new.save()
        test_new, test = self.copy_and_reset_test(id=finding.test.id)
        test_new.engagement = eng_new
        test_new.save()
        return test_new, eng_new

    def create_new_test_and_engagment_and_product_from_finding(self, finding):
        product_new, product = self.copy_and_reset_product(id=finding.test.engagement.product.id)
        product_new.save()
        eng_new, eng = self.copy_and_reset_engagement(id=finding.test.engagement.id)
        eng_new.product = product_new
        eng_new.save()
        test_new, test = self.copy_and_reset_test(id=finding.test.id)
        test_new.engagement = eng_new
        test_new.save()
        return test_new, eng_new, product_new

    def enable_false_positive_history(self):
        system_settings = System_Settings.objects.get()
        system_settings.false_positive_history = True
        system_settings.save()

    def enable_dedupe(self):
        system_settings = System_Settings.objects.get()
        system_settings.enable_deduplication = True
        system_settings.save()

    def disable_dedupe(self):
        system_settings = System_Settings.objects.get()
        system_settings.enable_deduplication = False
        system_settings.save()
