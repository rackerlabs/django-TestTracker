from django.test import TestCase
from dojo.tools.gitlab_api_fuzzing.parser import GitlabAPIFuzzingParser
from dojo.models import Test


class TestGitlabAPIFuzzingParser(TestCase):
    def test_gitlab_api_fuzzing_parser_with_no_vuln_has_no_findings(self):
        with open(
            "dojo/unittests/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_0_vuln.json"
        ) as testfile:
            parser = GitlabAPIFuzzingParser()
            findings = parser.get_findings(testfile, Test())
            testfile.close()
            self.assertEqual(0, len(findings))

    def test_gitlab_api_fuzzing_parser_with_one_criticle_vuln_has_one_findings(self):
        with open(
            "dojo/unittests/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_1_vuln.json"
        ) as testfile:
            parser = GitlabAPIFuzzingParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(1, len(findings))
            first_finding = findings[0]
            self.assertEqual(
                first_finding.title,
                "name - c83603d0befefe01644abdda1abbfaac842fccbabfbe336db9f370386e40f702",
            )
            self.assertEqual(
                first_finding.description,
                "coverage_fuzzing\nIndex-out-of-range\ngo-fuzzing-example.ParseComplex.func6\ngo-fuzzing-example.ParseComplex\ngo-fuzzing-example.Fuzz\n",
            )

    def test_gitlab_api_fuzzing_parser_with_invalid_json(self):
        with open(
            "dojo/unittests/scans/gitlab_api_fuzzing/gitlab_api_fuzzing_invalid.json"
        ) as testfile:
            with self.assertRaises(ValueError):
                parser = GitlabAPIFuzzingParser()
                parser.get_findings(testfile, Test())
