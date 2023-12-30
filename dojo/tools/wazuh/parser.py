import hashlib
import json
from dojo.models import Finding, Endpoint


class WazuhParser(object):
    """
    IMPORTANT: Please use the script available here https://github.com/quirinziessler/wazuh-findings-exporter to generate
    the report for DefectDojo. This script fetches the findings from wazuh based on a single Wazuh group. 
    In DD please configure one engagement per group and upload the report.

    The vulnerabilities with condition "Package unfixed" are skipped because there is no fix out yet.
    https://github.com/wazuh/wazuh/issues/14560
    """

    def get_scan_types(self):
        return ["Wazuh"]

    def get_label_for_scan_types(self, scan_type):
        return "Wazuh"

    def get_description_for_scan_types(self, scan_type):
        return "Wazuh"

    def get_findings(self, file, test):
        data = json.load(file)

        if not data:
            return []

        # Detect duplications
        dupes = dict()

        # Loop through each element in the list
        for entry in data:
            vulnerabilities = entry.get("data", {}).get("affected_items", [])
            for item in vulnerabilities:
                if (
                    item["condition"] != "Package unfixed"
                    and item["severity"] != "Untriaged"
                ):
                    id = item.get("cve")
                    package_name = item.get("name")
                    package_version = item.get("version")
                    description = item.get("condition")
                    severity = item.get("severity").capitalize()
                    agent_ip = item.get("agent_ip")
                    links = item.get("external_references")
                    cvssv3_score = item.get("cvss3_score")
                    publish_date = item.get("published")
                    agent_name = item.get("agent_name")

                    if links:
                        references = "\n".join(links)
                    else:
                        references = None

                    title = (
                        item.get("title") + " (version: " + package_version + ")"
                    )
                    dupe_key = title + id + agent_name + package_name + package_version
                    dupe_key = hashlib.sha256(dupe_key.encode('utf-8')).hexdigest()

                    if dupe_key in dupes:
                        find = dupes[dupe_key]
                    else:
                        dupes[dupe_key] = True

                        find = Finding(
                            title=title,
                            test=test,
                            description=description,
                            severity=severity,
                            mitigation="mitigation",
                            references=references,
                            static_finding=True,
                            component_name=package_name,
                            component_version=package_version,
                            cvssv3_score = cvssv3_score,
                            publish_date = publish_date,
                            unique_id_from_tool = dupe_key,
                        )
                        # in some cases the agent_ip is not the perfect way on how to identify a host. Thus prefer the agent_name, if existant.
                        if agent_ip and agent_name:
                            find.unsaved_endpoints = [Endpoint(host=agent_name)]
                        elif agent_ip:
                            find.unsaved_endpoints = [Endpoint(host=agent_ip)]
                        elif agent_name:
                            find.unsaved_endpoints = [Endpoint(host=agent_name)]
                        dupes[dupe_key] = find

        return list(dupes.values())