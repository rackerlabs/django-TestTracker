import json
from datetime import datetime
import hyperlink
from dojo.models import Finding, Endpoint


class GitlabDastParser(object):
    """
    Import GitLab DAST Report in JSON format
    """

    def get_scan_types(self):
        return ["GitLab DAST Report"]

    def get_label_for_scan_types(self, scan_type):
        return "GitLab DAST Report"

    def get_description_for_scan_types(self, scan_type):
        return "GitLab DAST Report in JSON format (option --json)."

    # turning a json file to string
    def parse_json(self, file):
        data = file.read()
        try:
            tree = json.loads(str(data, 'utf-8'))
        except:
            tree = json.loads(data)

        return tree

    def get_items(self, tree, test):
        items = {}

        # iterating through each vulnerability
        for node in tree['vulnerabilities']:
            item = get_item(node, test)
            if item:
                items[item.unique_id_from_tool] = item

        return list(items.values())

    def get_findings(self, file, test):
        if file is None:
            return None

        tree = self.parse_json(file)
        if tree:
            return self.get_items(tree, test)

    def convert_severity(self, num_severity):
        """Convert severity value"""
        if num_severity >= -10:
            return "Low"
        elif -11 >= num_severity > -26:
            return "Medium"
        elif num_severity <= -26:
            return "High"
        else:
            return "Info"


# iterating through properties of each vulnerability
def get_item(vuln, test):

    if vuln["category"] != "dast":
        return None

    # scanner_confidence
    scanner_confidence = get_confidence_numeric(vuln["confidence"])

    # id
    if "id" in vuln:
        unique_id_from_tool = vuln["id"]
    else:  # deprecated
        unique_id_from_tool = vuln["cve"]

    # title
    if "name" in vuln:
        title = vuln["name"]
    # fallback to using id as a title
    else:
        title = unique_id_from_tool

    # description
    description = f"Scanner: {vuln['scanner']['name']}\n"
    if "message" in vuln:
        description += f"{vuln['message']}\n"
    elif "description" in vuln:
        description += f"{vuln['description']}\n"

    # date
    if "discovered_at" in vuln:
        date = datetime.strptime(vuln["discovered_at"], "%Y-%m-%dT%H:%M:%S.%f")
    else:
        date = None

    # endpoint
    location = vuln["location"]
    if "hostname" in location and "path" in location:
        url_str = f"{location['hostname']}{location['path']}"
        url = hyperlink.parse(url_str)
        endpoint = Endpoint.from_uri(url)
        print("Using url as an arg:")
        print("Endpoint: " + str(endpoint))

        print("Using str as an arg:")
        endpoint2 = Endpoint.from_uri(url_str)
        print("Endpoint: " + str(endpoint2))
    else:
        endpoint = None

    # TODO: found_by

    # severity
    severity = ""
    if "severity" in vuln:
        severity = vuln["severity"]

    if "solution" in vuln:
        mitigation = vuln["solution"]

    cve = vuln["cve"]
    cwe = 0

    references = ""
    for ref in vuln["identifiers"]:
        if ref["type"].lower() == "cwe":
            cwe = int(ref["value"])
        else:
            references += f"Identifier type: {ref['type']}\n"
            references += f"Name: {ref['name']}\n"
            references += f"Value: {ref['value']}\n"
            if "url" in ref:
                references += f"URL: {ref['url']}\n"
            references += '\n'

    finding = Finding(
        test=test,  # Test
        unique_id_from_tool=unique_id_from_tool,  # str
        scanner_confidence=scanner_confidence,  # int
        title=title,  # str
        description=description,  # str
        date=date,  # datetime object
        references=references,  # str (identifiers)
        mitigation=mitigation,  # str (solution)
        cve=cve  # str
    )

    if severity:
        finding.severity = severity
    if cwe != 0:
        finding.cwe = cwe
    finding.unsaved_endpoints = [endpoint]

    return finding


def get_confidence_numeric(confidence):
    switcher = {
        'Confirmed': 1,     # Certain
        'High': 3,          # Firm
        'Medium': 4,        # Firm
        'Low': 6,           # Tentative
        'Experimental': 7,  # Tentative
        'Unknown': 8,       # Tentative
        'Ignore': 10,       # Tentative
    }
    return switcher.get(confidence, None)
