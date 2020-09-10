from django import template
from dojo.models import Endpoint_Status
register = template.Library()


@register.filter(name='get_vulnerable_endpoints')
def get_vulnerable_endpoints(finding):
    status_list = finding.endpoint_status.all().filter(mitigated=False)
    return [status.endpoint for status in status_list]


@register.filter(name='get_mitigated_endpoints')
def get_mitigated_endpoints(finding):
    status_list = finding.endpoint_status.all().filter(mitigated=True)
    return [status.endpoint for status in status_list]


@register.filter
def vulnerable_endpoint_count(finding):
    return finding.endpoint_status.all().filter(mitigated=False).count()


@register.filter
def mitigated_endpoint_count(finding):
    return finding.endpoint_status.all().filter(mitigated=True).count()


@register.filter
def endpoint_display_status(endpoint, finding):
    status = Endpoint_Status.objects.get(endpoint=endpoint, finding=finding)
    if status.false_positive:
        return "False Positive"
    if status.risk_accepted:
        return "Risk Accepted"
    if status.out_of_scope:
        return "Out of Scope"
    if status.mitigated:
        return "Mitigated"
    return "Active"


@register.filter
def endpoint_update_time(endpoint, finding):
    status = Endpoint_Status.objects.get(endpoint=endpoint, finding=finding)
    return status.last_modified


@register.filter
def endpoint_date(endpoint, finding):
    status = Endpoint_Status.objects.get(endpoint=endpoint, finding=finding)
    return status.date


@register.filter
def endpoint_mitigator(endpoint, finding):
    status = Endpoint_Status.objects.get(endpoint=endpoint, finding=finding)
    return status.mitigated_by


@register.filter
def endpoint_mitigated_time(endpoint, finding):
    status = Endpoint_Status.objects.get(endpoint=endpoint, finding=finding)
    return status.mitigated_time


@register.filter
def endpoint_check_active(endpoint, finding):
    status = Endpoint_Status.objects.get(endpoint=endpoint, finding=finding)
    return not status.mitigated
