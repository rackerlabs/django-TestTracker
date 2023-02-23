from ..dojo_test_case import DojoTestCase
from dojo.tools.wazuh.parser import WazuhParser
from dojo.models import Test


class TestWazuhParser(DojoTestCase):

    def test_parse_no_findings(self):
        testfile = open("unittests/scans/wazuh/no_findings.json")
        parser = WazuhParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_one_finding(self):
        testfile = open("unittests/scans/wazuh/one_finding.json")
        parser = WazuhParser()
        findings = parser.get_findings(testfile, Test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))

    def test_parse_many_finding(self):
        testfile = open("unittests/scans/wazuh/many_findings.json")
        parser = WazuhParser()
        findings = parser.get_findings(testfile, Test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(7, len(findings))
