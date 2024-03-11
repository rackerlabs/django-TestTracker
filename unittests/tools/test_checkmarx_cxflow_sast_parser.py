from dojo.models import Product, Engagement, Test
from dojo.tools.checkmarx_cxflow_sast.parser import CheckmarxCXFlowSastParser
from ..dojo_test_case import DojoTestCase, get_unit_tests_path

import dateutil.parser


class TestCheckmarxCxflowSast(DojoTestCase):

    def init(self, reportFilename):
        my_file_handle = open(reportFilename)
        product = Product()
        engagement = Engagement()
        test = Test()
        engagement.product = product
        test.engagement = engagement
        return my_file_handle, product, engagement, test

    def test_file_name_aggregated_parse_file_with_no_vulnerabilities_has_no_findings(self):
        my_file_handle, product, engagement, test = self.init(
            get_unit_tests_path() + "/scans/checkmarx_cxflow_sast/no_finding.json"
        )
        parser = CheckmarxCXFlowSastParser()
        findings = parser.get_findings(my_file_handle, test)
        self.assertEqual(0, len(findings))

    def test_file_name_aggregated_parse_file_with_no_vulnerabilities_has_1_finding(self):
        my_file_handle, product, engagement, test = self.init(
            get_unit_tests_path() + "/scans/checkmarx_cxflow_sast/1-finding.json"
        )
        parser = CheckmarxCXFlowSastParser()
        findings = parser.get_findings(my_file_handle, test)
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("Reflected XSS All Clients", finding.title)
        self.assertEqual(79, finding.cwe1)
        self.assertEqual(dateutil.parser.parse("Sunday, January 19, 2020 2:40:11 AM"), finding.)
