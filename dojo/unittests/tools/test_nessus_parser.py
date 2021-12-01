from os import path
from django.test import TestCase
from dojo.tools.nessus.parser import NessusXMLParser, NessusCSVParser, NessusParser
from dojo.models import Finding, Test, Engagement, Product


class TestNessusParser(TestCase):
    def create_test(self):
        test = Test()
        test.engagement = Engagement()
        test.engagement.product = Product()
        return test

    def test_parse_some_findings(self):
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln.xml"))
        parser = NessusXMLParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(6, len(findings))
        finding = findings[5]
        self.assertEqual("Info", finding.severity)
        self.assertIsNone(finding.cwe)
        print(finding.unsaved_endpoints)
        endpoint = finding.unsaved_endpoints[0]
        self.assertEqual("https", endpoint.protocol)
        endpoint = finding.unsaved_endpoints[1]
        self.assertEqual("tcp", endpoint.protocol)

    def test_parse_some_findings_csv(self):
        """Test one report provided by a user"""
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln.csv"))
        parser = NessusCSVParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(4, len(findings))
        for i in [0, 1, 2, 3]:
            finding = findings[i]
            self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual("Medium", finding.severity)
            self.assertEqual(0, finding.cwe)
        # check some data
        finding = findings[0]
        self.assertEqual("CVE-2004-2761", finding.cve)
        self.assertEqual(1, len(finding.unsaved_endpoints))
        self.assertEqual("10.1.1.1", finding.unsaved_endpoints[0].host)
        self.assertEqual("AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N/E:P/RL:O/RC:C", finding.cvssv3)
        # TODO work on component attributes for Nessus CSV parser
        self.assertIsNotNone(finding.component_name)
        self.assertEqual("md5", finding.component_name)
        # this vuln have 'CVE-2013-2566,CVE-2015-2808' as CVE
        # current implementation return the first
        finding = findings[3]
        self.assertEqual("CVE-2013-2566", finding.cve)

    def test_parse_some_findings_csv2(self):
        """Test that use default columns of Nessus Pro 8.13.1 (#257)"""
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln2-default.csv"))
        parser = NessusCSVParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(29, len(findings))
        finding = findings[0]
        self.assertIn(finding.severity, Finding.SEVERITIES)
        self.assertEqual("Info", finding.severity)
        self.assertIsNone(finding.cve)
        self.assertEqual(0, finding.cwe)
        self.assertEqual("HTTP Server Type and Version", finding.title)
        finding = findings[25]
        self.assertIn(finding.severity, Finding.SEVERITIES)
        self.assertEqual("SSL Certificate Signed Using Weak Hashing Algorithm (Known CA)", finding.title)
        self.assertEqual("Info", finding.severity)
        self.assertEqual("CVE-2004-2761", finding.cve)

    def test_parse_some_findings_csv2_all(self):
        """Test that use a report with all columns of Nessus Pro 8.13.1 (#257)"""
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln2-all.csv"))
        parser = NessusCSVParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(29, len(findings))
        finding = findings[0]
        self.assertIn(finding.severity, Finding.SEVERITIES)
        self.assertEqual("Info", finding.severity)
        self.assertIsNone(finding.cve)
        self.assertEqual(0, finding.cwe)
        self.assertEqual("HTTP Server Type and Version", finding.title)
        finding = findings[25]
        self.assertIn(finding.severity, Finding.SEVERITIES)
        self.assertEqual("SSL Certificate Signed Using Weak Hashing Algorithm (Known CA)", finding.title)
        self.assertEqual("Info", finding.severity)
        self.assertEqual("CVE-2004-2761", finding.cve)

    def test_parse_some_findings_csv_bytes(self):
        """This tests is designed to test the parser with different read modes"""
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln2-all.csv"))
        parser = NessusCSVParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln2-all.csv"), "rt")
        parser = NessusCSVParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_many_vuln2-all.csv"), "rb")
        parser = NessusCSVParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()

    def test_parse_some_findings_samples(self):
        """Test that come from samples repo"""
        testfile = open(path.join(path.dirname(__file__), "../scans/nessus/nessus_v_unknown.xml"))
        parser = NessusParser()
        findings = parser.get_findings(testfile, self.create_test())
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(32, len(findings))
        finding = findings[0]
        self.assertIn(finding.severity, Finding.SEVERITIES)
        self.assertEqual("Info", finding.severity)
        self.assertIsNone(finding.cve)
        self.assertEqual("Nessus Scan Information", finding.title)
        finding = findings[25]
        self.assertIn(finding.severity, Finding.SEVERITIES)
        self.assertEqual("Nessus SYN scanner", finding.title)
        self.assertEqual("Info", finding.severity)
        self.assertIsNone(finding.cve)
        endpoint = finding.unsaved_endpoints[26]
        self.assertEqual("http", endpoint.protocol)
        endpoint = finding.unsaved_endpoints[37]
        self.assertEqual("tcp", endpoint.protocol)
