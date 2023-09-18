from ..dojo_test_case import DojoParserTestCase, get_unit_tests_path
from dojo.tools.gitlab_api_fuzzing.parser import GitlabAPIFuzzingParser
from dojo.models import Test


class TestGitlabAPIFuzzingParser(DojoParserTestCase):

    parser = GitlabAPIFuzzingParser()

    def test_gitlab_api_fuzzing_parser_with_no_vuln_has_no_findings(self):
        with open(f"{get_unit_tests_path()}/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_0_vuln.json") as testfile:
            findings = self.parser.get_findings(testfile, Test())
            testfile.close()
            self.assertEqual(0, len(findings))

    def test_gitlab_api_fuzzing_parser_with_one_criticle_vuln_has_one_findings_v14(self):
        with open(f"{get_unit_tests_path()}/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_1_vuln_v14.json") as testfile:
            findings = self.parser.get_findings(testfile, Test())
            self.assertEqual(1, len(findings))
            first_finding = findings[0]
            self.assertEqual(first_finding.title, "name")
            self.assertEqual(
                first_finding.description,
                "coverage_fuzzing\nIndex-out-of-range\ngo-fuzzing-example.ParseComplex.func6\ngo-fuzzing-example.ParseComplex\ngo-fuzzing-example.Fuzz\n",
            )
            self.assertEqual(
                first_finding.unique_id_from_tool,
                "c83603d0befefe01644abdda1abbfaac842fccbabfbe336db9f370386e40f702",
            )

    def test_gitlab_api_fuzzing_parser_with_one_criticle_vuln_has_one_findings_v15(self):
        with open(f"{get_unit_tests_path()}/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_1_vuln_v15.json") as testfile:
            findings = self.parser.get_findings(testfile, Test())
            self.assertEqual(1, len(findings))
            first_finding = findings[0]
            self.assertEqual(first_finding.title, "name")
            self.assertEqual(
                first_finding.description,
                "\nIndex-out-of-range\ngo-fuzzing-example.ParseComplex.func6\ngo-fuzzing-example.ParseComplex\ngo-fuzzing-example.Fuzz\n",
            )
            self.assertEqual(
                first_finding.unique_id_from_tool,
                "c83603d0befefe01644abdda1abbfaac842fccbabfbe336db9f370386e40f702",
            )

    def test_gitlab_api_fuzzing_parser_with_invalid_json(self):
        with open(f"{get_unit_tests_path()}/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_invalid.json") as testfile:
            # Something is wrong with JSON file
            with self.assertRaises((KeyError, ValueError)):
                self.parser.get_findings(testfile, Test())
