import json

from dojo.models import Finding


class PipAuditParser:

    def get_scan_types(self):
        return ["pip-audit Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "pip-audit Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Import pip-audit JSON scan report."

    def requires_file(self, scan_type):
        return True

    def get_findings(self, scan_file, test):

        scan_data = scan_file.read()
        try:
            data = json.loads(str(scan_data, 'utf-8'))
        except:
            data = json.loads(scan_data)

        findings = list()
        for item in data:
            vulnerabilities = item.get('vulns', [])
            if vulnerabilities:
                component_name = item['name']
                component_version = item.get('version', None)
                for vulnerability in vulnerabilities:
                    vuln_id = vulnerability.get('id', None)
                    vuln_fix_versions = vulnerability.get('fix_versions', None)
                    vuln_description = vulnerability.get('description', None)

                    title = f'{vuln_id} in {component_name}:{component_version}'

                    description = f'**Id:** {vuln_id}'
                    description += f'\n**Description:** {vuln_description}'

                    if vuln_id.startswith('CVE'):
                        cve = vuln_id
                    else:
                        cve = None

                    mitigation = None
                    if vuln_fix_versions:
                        mitigation = 'Upgrade to version:'
                        if len(vuln_fix_versions) == 1:
                            mitigation += f' {vuln_fix_versions[0]}'
                        else:
                            for fix_version in vuln_fix_versions:
                                mitigation += f'\n- {fix_version}'

                    findings.append(
                        Finding(
                            test=test,
                            title=title,
                            cve=cve,
                            cwe=1352,
                            severity='Medium',
                            description=description,
                            mitigation=mitigation,
                            component_name=component_name,
                            component_version=component_version,
                            static_finding=True,
                            dynamic_finding=False,
                        )
                    )

        return findings
