from .dojo_test_case import DojoTestCase
from dojo.tools.outpost24.parser import Outpost24Parser
from dojo.models import Test


class TestOutpost24Parser(DojoTestCase):
    def assert_file_has_n_items(self, filename, item_count):
        with open(filename) as file:
            parser = Outpost24Parser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEquals(item_count, len(findings))
            if item_count > 0:
                for item in findings:
                    endpoint_count = len(item.unsaved_endpoints)
                    self.assertGreater(endpoint_count, 0)

    def test_parser_no_items(self):
        self.assert_file_has_n_items(self.unit_test_folder + "/scans/outpost24/none.xml", 0)

    def test_parser_one_item(self):
        self.assert_file_has_n_items(self.unit_test_folder + "/scans/outpost24/one.xml", 1)

    def test_parser_sample_items(self):
        self.assert_file_has_n_items(self.unit_test_folder + "/scans/outpost24/sample.xml", 24)
