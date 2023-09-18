from ..dojo_test_case import DojoParserTestCase
from dojo.tools.h1.parser import H1Parser
from dojo.models import Test


class TestHackerOneParser(DojoParserTestCase):

    parser = H1Parser()

    def test_parse_file_with_no_vuln_has_no_finding(self):
        testfile = open("unittests/scans/h1/data_empty.json")
        findings = self.parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_file_with_one_vuln_has_one_finding(self):
        testfile = open("unittests/scans/h1/data_one.json")
        findings = self.parser.get_findings(testfile, Test())
        self.assertEqual(1, len(findings))

    def test_parse_file_with_multiple_vuln_has_multiple_finding(self):
        testfile = open("unittests/scans/h1/data_many.json")
        findings = self.parser.get_findings(testfile, Test())
        self.assertEqual(2, len(findings))
