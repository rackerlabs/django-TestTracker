from django.test import TestCase

from dojo.models import Test, Product, Engagement
from dojo.tools.ptart.parser import PTARTParser


class TestPTARTParser(TestCase):

    def setUp(self):
        self.product = Product(name="sample product",
                               description="what a description")
        self.engagement = Engagement(name="sample engagement",
                                     product=self.product)
        self.test = Test(engagement=self.engagement)

    def test_ptart_parser_tools_parse_ptart_severity(self):
        from dojo.tools.ptart.ptart_parser_tools import parse_ptart_severity
        with self.subTest("Critical"):
            self.assertEqual("Critical", parse_ptart_severity(1))
        with self.subTest("High"):
            self.assertEqual("High", parse_ptart_severity(2))
        with self.subTest("Medium"):
            self.assertEqual("Medium", parse_ptart_severity(3))
        with self.subTest("Low"):
            self.assertEqual("Low", parse_ptart_severity(4))
        with self.subTest("Info"):
            self.assertEqual("Info", parse_ptart_severity(5))
        with self.subTest("Unknown"):
            self.assertEqual("Info", parse_ptart_severity(6))

    def test_ptart_parser_tools_parse_ptart_fix_effort(self):
        from dojo.tools.ptart.ptart_parser_tools import parse_ptart_fix_effort
        with self.subTest("High"):
            self.assertEqual("High", parse_ptart_fix_effort(1))
        with self.subTest("Medium"):
            self.assertEqual("Medium", parse_ptart_fix_effort(2))
        with self.subTest("Low"):
            self.assertEqual("Low", parse_ptart_fix_effort(3))
        with self.subTest("Unknown"):
            self.assertEqual(None, parse_ptart_fix_effort(4))

    def test_ptart_parser_tools_parse_title_from_hit(self):
        from dojo.tools.ptart.ptart_parser_tools import parse_title_from_hit
        with self.subTest("Title and ID"):
            self.assertEqual("1234: Test Title", parse_title_from_hit({"title": "Test Title", "id": "1234"}))
        with self.subTest("Title Only"):
            self.assertEqual("Test Title", parse_title_from_hit({"title": "Test Title"}))
        with self.subTest("ID Only"):
            self.assertEqual("1234", parse_title_from_hit({"id": "1234"}))
        with self.subTest("No Title or ID"):
            self.assertEqual("Unknown Hit", parse_title_from_hit({}))
        with self.subTest("Empty Title"):
            self.assertEqual("Unknown Hit", parse_title_from_hit({"title": ""}))
        with self.subTest("Empty ID"):
            self.assertEqual("Unknown Hit", parse_title_from_hit({"id": ""}))
        with self.subTest("Blank Title and Blank ID"):
            self.assertEqual("Unknown Hit", parse_title_from_hit({"title": "", "id": ""}))
        with self.subTest("Blank Title and Non-blank id"):
            self.assertEqual("1234", parse_title_from_hit({"title": "", "id": "1234"}))
        with self.subTest("Non-blank Title and Blank id"):
            self.assertEqual("Test Title", parse_title_from_hit({"title": "Test Title", "id": ""}))

    def test_cvss_vector_acquisition(self):
        from dojo.tools.ptart.ptart_parser_tools import parse_cvss_vector
        with self.subTest("Test CVSSv3 Vector"):
            hit = {
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"
            }
            self.assertEqual("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", parse_cvss_vector(hit, 3))
        with self.subTest("Test CVSSv4 Vector"):
            hit = {
                "cvss_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N"
            }
            self.assertEqual(None, parse_cvss_vector(hit, 4))
        with self.subTest("Test CVSSv3 Vector with CVSSv4 Request"):
            hit = {
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"
            }
            self.assertEqual(None, parse_cvss_vector(hit, 4))
        with self.subTest("Test CVSSv4 Vector with CVSSv3 Request"):
            hit = {
                "cvss_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N"
            }
            self.assertEqual(None, parse_cvss_vector(hit, 3))
        with self.subTest("Test No CVSS Vector"):
            hit = {}
            self.assertEqual(None, parse_cvss_vector(hit, 3))
        with self.subTest("Test CVSSv2 Vector"):
            hit = {
                "cvss_vector": "CVSS:2.0/AV:N/AC:L/Au:N/C:C/I:C/A:C"
            }
            self.assertEqual(None, parse_cvss_vector(hit, 2))
        with self.subTest("Test Blank CVSS Vector"):
            hit = {
                "cvss_vector": ""
            }
            self.assertEqual(None, parse_cvss_vector(hit, 3))

    def test_ptart_parser_with_empty_json_throws_error(self):
        with self.assertRaises(ValueError) as context:
            with open("unittests/scans/ptart/empty_with_error.json") as testfile:
                parser = PTARTParser()
                parser.get_findings(testfile, self.test)
                self.assertTrue("Parse Error: assessments key not found in the report" in str(context.exception))

    def test_ptart_parser_with_no_assessments_has_no_findings(self):
        with open("unittests/scans/ptart/ptart_zero_vul.json") as testfile:
            parser = PTARTParser()
            findings = parser.get_findings(testfile, self.test)
            self.assertEqual(0, len(findings))
            self.assertEqual([], findings)

    def test_ptart_parser_with_one_assessment_has_one_finding(self):
        with open("unittests/scans/ptart/ptart_one_vul.json") as testfile:
            parser = PTARTParser()
            findings = parser.get_findings(testfile, self.test)
            self.assertEqual(1, len(findings))
            with self.subTest("Test Assessment: Broken Access Control"):
                finding = findings[0]
                self.assertEqual("PTART-2024-00002: Broken Access Control", finding.title)
                self.assertEqual("High", finding.severity)
                self.assertEqual("Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification or destruction of all data, or performing a business function outside of the limits of the user.", finding.description)
                self.assertEqual("Access control vulnerabilities can generally be prevented by taking a defense-in-depth approach and applying the following principles:\n\n* Never rely on obfuscation alone for access control.\n* Unless a resource is intended to be publicly accessible, deny access by default.\n* Wherever possible, use a single application-wide mechanism for enforcing access controls.\n* At the code level, make it mandatory for developers to declare the access that is allowed for each resource, and deny access by default.\n* Thoroughly audit and test access controls to ensure they are working as designed.", finding.mitigation)
                self.assertEqual(("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",), finding.cvssv3)
                self.assertEqual(("PTART-2024-00002",), finding.unique_id_from_tool)
                self.assertEqual("Low", finding.effort_for_fixing)
                self.assertEqual("Test Assessment", finding.component_name)
                self.assertEqual("2024-09-06", finding.date.strftime("%Y-%m-%d"))
                self.assertEqual(2, len(finding.unsaved_tags))
                self.assertEqual([
                    "A01:2021-Broken Access Control",
                    "A04:2021-Insecure Design"
                ], finding.unsaved_tags)
                self.assertEqual(1, len(finding.unsaved_endpoints))
                endpoint = finding.unsaved_endpoints[0]
                self.assertEqual(str(endpoint), "https://test.example.com")
                self.assertEqual(2, len(finding.unsaved_files))
                screenshot = finding.unsaved_files[0]
                self.assertEqual("Borked.png", screenshot["title"])
                self.assertTrue(screenshot["data"].startswith("iVBORw0KGgoAAAAN"), "Invalid Screenshot Data")
                attachment = finding.unsaved_files[1]
                self.assertEqual("License", attachment["title"])
                self.assertTrue(attachment["data"].startswith("TUlUIExpY2Vuc2UKCkNvcHl"), "Invalid Attachment Data")

    def test_ptart_parser_with_one_assessment_has_many_findings(self):
        with open("unittests/scans/ptart/ptart_many_vul.json") as testfile:
            parser = PTARTParser()
            findings = parser.get_findings(testfile, self.test)
            self.assertEqual(2, len(findings))
            with self.subTest("Test Assessment: Broken Access Control"):
                finding = findings[0]
                self.assertEqual("PTART-2024-00002: Broken Access Control", finding.title)
                self.assertEqual("High", finding.severity)
                self.assertEqual("Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification or destruction of all data, or performing a business function outside of the limits of the user.", finding.description)
                self.assertEqual("Access control vulnerabilities can generally be prevented by taking a defense-in-depth approach and applying the following principles:\n\n* Never rely on obfuscation alone for access control.\n* Unless a resource is intended to be publicly accessible, deny access by default.\n* Wherever possible, use a single application-wide mechanism for enforcing access controls.\n* At the code level, make it mandatory for developers to declare the access that is allowed for each resource, and deny access by default.\n* Thoroughly audit and test access controls to ensure they are working as designed.", finding.mitigation)
                self.assertEqual(("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",), finding.cvssv3)
                self.assertEqual(("PTART-2024-00002",), finding.unique_id_from_tool)
                self.assertEqual("Low", finding.effort_for_fixing)
                self.assertEqual("Test Assessment", finding.component_name)
                self.assertEqual("2024-09-06", finding.date.strftime("%Y-%m-%d"))
                self.assertEqual(1, len(finding.unsaved_endpoints))
                endpoint = finding.unsaved_endpoints[0]
                self.assertEqual(str(endpoint), "https://test.example.com")
                self.assertEqual(2, len(finding.unsaved_files))
                screenshot = finding.unsaved_files[0]
                self.assertEqual("Borked.png", screenshot["title"])
                self.assertTrue(screenshot["data"].startswith("iVBORw0KGgoAAAAN"), "Invalid Screenshot Data")
                attachment = finding.unsaved_files[1]
                self.assertEqual("License", attachment["title"])
                self.assertTrue(attachment["data"].startswith("TUlUIExpY2Vuc2UKCkNvcHl"), "Invalid Attachment Data")
            with self.subTest("Test Assessment: Unrated Hit"):
                finding = findings[1]
                self.assertEqual("PTART-2024-00003: Unrated Hit", finding.title)
                self.assertEqual("Info", finding.severity)
                self.assertEqual("Some hits are not rated.", finding.description)
                self.assertEqual("They can be informational or not related to a direct attack", finding.mitigation)
                self.assertEqual(None, finding.cvssv3)
                self.assertEqual(("PTART-2024-00003",), finding.unique_id_from_tool)
                self.assertEqual("Low", finding.effort_for_fixing)
                self.assertEqual("Test Assessment", finding.component_name)
                self.assertEqual("2024-09-06", finding.date.strftime("%Y-%m-%d"))

    def test_ptart_parser_with_multiple_assessments_has_many_findings_correctly_grouped(self):
        with open("unittests/scans/ptart/ptart_vulns_with_mult_assessments.json") as testfile:
            parser = PTARTParser()
            findings = parser.get_findings(testfile, self.test)
            self.assertEqual(3, len(findings))
            with self.subTest("Test Assessment: Broken Access Control"):
                finding = next((f for f in findings if f.unique_id_from_tool[0] == "PTART-2024-00002"), None)
                self.assertEqual("PTART-2024-00002: Broken Access Control", finding.title)
                self.assertEqual("High", finding.severity)
                self.assertEqual("Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification or destruction of all data, or performing a business function outside of the limits of the user.", finding.description)
                self.assertEqual("Access control vulnerabilities can generally be prevented by taking a defense-in-depth approach and applying the following principles:\n\n* Never rely on obfuscation alone for access control.\n* Unless a resource is intended to be publicly accessible, deny access by default.\n* Wherever possible, use a single application-wide mechanism for enforcing access controls.\n* At the code level, make it mandatory for developers to declare the access that is allowed for each resource, and deny access by default.\n* Thoroughly audit and test access controls to ensure they are working as designed.", finding.mitigation)
                self.assertEqual(("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",), finding.cvssv3)
                self.assertEqual(("PTART-2024-00002",), finding.unique_id_from_tool)
                self.assertEqual("Low", finding.effort_for_fixing)
                self.assertEqual("Test Assessment", finding.component_name)
                self.assertEqual("2024-09-06", finding.date.strftime("%Y-%m-%d"))
                self.assertEqual(1, len(finding.unsaved_endpoints))
                endpoint = finding.unsaved_endpoints[0]
                self.assertEqual(str(endpoint), "https://test.example.com")
                self.assertEqual(2, len(finding.unsaved_files))
                screenshot = finding.unsaved_files[0]
                self.assertEqual("Borked.png", screenshot["title"])
                self.assertTrue(screenshot["data"].startswith("iVBORw0KGgoAAAAN"), "Invalid Screenshot Data")
                attachment = finding.unsaved_files[1]
                self.assertEqual("License", attachment["title"])
                self.assertTrue(attachment["data"].startswith("TUlUIExpY2Vuc2UKCkNvcHl"), "Invalid Attachment Data")
            with self.subTest("Test Assessment: Unrated Hit"):
                finding = next((f for f in findings if f.unique_id_from_tool[0] == "PTART-2024-00003"), None)
                self.assertEqual("PTART-2024-00003: Unrated Hit", finding.title)
                self.assertEqual("Info", finding.severity)
                self.assertEqual("Some hits are not rated.", finding.description)
                self.assertEqual("They can be informational or not related to a direct attack", finding.mitigation)
                self.assertEqual(None, finding.cvssv3)
                self.assertEqual(("PTART-2024-00003",), finding.unique_id_from_tool)
                self.assertEqual("Low", finding.effort_for_fixing)
                self.assertEqual("Test Assessment", finding.component_name)
                self.assertEqual("2024-09-06", finding.date.strftime("%Y-%m-%d"))
            with self.subTest("New Api: HTML Injection"):
                finding = next((f for f in findings if f.unique_id_from_tool[0] == "PTART-2024-00004"), None)
                self.assertEqual("PTART-2024-00004: HTML Injection", finding.title)
                self.assertEqual("Low", finding.severity)
                self.assertEqual("HTML injection is a type of injection issue that occurs when a user is able to control an input point and is able to inject arbitrary HTML code into a vulnerable web page. This vulnerability can have many consequences, like disclosure of a user's session cookies that could be used to impersonate the victim, or, more generally, it can allow the attacker to modify the page content seen by the victims.", finding.description)
                self.assertEqual("Preventing HTML injection is trivial in some cases but can be much harder depending on the complexity of the application and the ways it handles user-controllable data.\n\nIn general, effectively preventing HTML injection vulnerabilities is likely to involve a combination of the following measures:\n\n* **Filter input on arrival**. At the point where user input is received, filter as strictly as possible based on what is expected or valid input.\n* **Encode data on output**. At the point where user-controllable data is output in HTTP responses, encode the output to prevent it from being interpreted as active content. Depending on the output context, this might require applying combinations of HTML, URL, JavaScript, and CSS encoding.", finding.mitigation)
                self.assertEqual(("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N",), finding.cvssv3)
                self.assertEqual(("PTART-2024-00004",), finding.unique_id_from_tool)
                self.assertEqual("Medium", finding.effort_for_fixing)
                self.assertEqual("New API", finding.component_name)
                self.assertEqual("2024-09-06", finding.date.strftime("%Y-%m-%d"))
                self.assertEqual(0, len(finding.unsaved_endpoints))
                self.assertEqual(0, len(finding.unsaved_files))

    #
    #
    # def test_ptart_parser_with_no_vuln_has_no_findings(self):
    #     testfile = open("unittests/scans/ptart/ptart_zero_vul.json")
    #     parser = PTARTParser()
    #     findings = parser.get_findings(testfile, self.test)
    #     testfile.close()
    #     self.assertEqual(0, len(findings))
    #
    # def test_ptart_parser_with_one_criticle_vuln_has_one_findings(self):
    #     testfile = open("unittests/scans/ptart/ptart_one_vul.json")
    #     parser = PTARTParser()
    #     findings = parser.get_findings(testfile, Test())
    #     testfile.close()
    #     for finding in findings:
    #         for endpoint in finding.unsaved_endpoints:
    #             endpoint.clean()
    #     self.assertEqual(1, len(findings))
    #     self.assertEqual("handlebars", findings[0].component_name)
    #     self.assertEqual("4.5.2", findings[0].component_version)
    #
    # def test_ptart_parser_with_many_vuln_has_many_findings(self):
    #     testfile = open("unittests/scans/ptart/ptart_many_vul.json")
    #     parser = PTARTParser()
    #     findings = parser.get_findings(testfile, Test())
    #     testfile.close()
    #     for finding in findings:
    #         for endpoint in finding.unsaved_endpoints:
    #             endpoint.clean()
    #     self.assertEqual(3, len(findings))
    #
    # def test_ptart_parser_empty_with_error(self):
    #     with self.assertRaises(ValueError) as context:
    #         testfile = open("unittests/scans/ptart/empty_with_error.json")
    #         parser = PTARTParser()
    #         findings = parser.get_findings(testfile, Test())
    #         testfile.close()
    #         for finding in findings:
    #             for endpoint in finding.unsaved_endpoints:
    #                 endpoint.clean()
    #         self.assertTrue(
    #             "PTART report contains errors:" in str(context.exception)
    #         )
    #         self.assertTrue("ECONNREFUSED" in str(context.exception))
