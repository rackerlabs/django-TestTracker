from crum import get_current_user
from django.conf import settings
from django.db.models import Exists, OuterRef, Q
from dojo.models import Endpoint, Endpoint_Status, Product_Member, Product_Type_Member
from dojo.authorization.authorization import get_roles_for_permission


def get_authorized_endpoints(permission):
    user = get_current_user()

    if user is None:
        return Endpoint.objects.none()

    if user.is_superuser:
        return Endpoint.objects.all()

    if settings.FEATURE_AUTHORIZATION_V2:
        if user.is_staff and settings.AUTHORIZATION_STAFF_OVERRIDE:
            return Endpoint.objects.all()

        roles = get_roles_for_permission(permission)
        authorized_product_type_roles = Product_Type_Member.objects.filter(
            product_type=OuterRef('product__prod_type_id'),
            user=user,
            role__in=roles)
        authorized_product_roles = Product_Member.objects.filter(
            product=OuterRef('product_id'),
            user=user,
            role__in=roles)
        endpoints = Endpoint.objects.annotate(
            product__prod_type__member=Exists(authorized_product_type_roles),
            product__member=Exists(authorized_product_roles))
        endpoints = endpoints.filter(
            Q(product__prod_type__member=True) |
            Q(product__member=True))
    else:
        if user.is_staff:
            endpoints = Endpoint.objects.all()
        else:
            endpoints = Endpoint.objects.filter(
                Q(product__authorized_users__in=[user]) |
                Q(product__prod_type__authorized_users__in=[user]))
    return endpoints


def get_authorized_endpoint_status(permission):
    user = get_current_user()

    if user is None:
        return Endpoint_Status.objects.none()

    if user.is_superuser:
        return Endpoint_Status.objects.all()

    if settings.FEATURE_AUTHORIZATION_V2:
        if user.is_staff and settings.AUTHORIZATION_STAFF_OVERRIDE:
            return Endpoint_Status.objects.all()

        roles = get_roles_for_permission(permission)
        authorized_product_type_roles = Product_Type_Member.objects.filter(
            product_type=OuterRef('endpoint__product__prod_type_id'),
            user=user,
            role__in=roles)
        authorized_product_roles = Product_Member.objects.filter(
            product=OuterRef('endpoint__product_id'),
            user=user,
            role__in=roles)
        endpoints = Endpoint_Status.objects.annotate(
            endpoint__product__prod_type__member=Exists(authorized_product_type_roles),
            endpoint__product__member=Exists(authorized_product_roles))
        endpoints = endpoints.filter(
            Q(endpoint__product__prod_type__member=True) |
            Q(endpoint__product__member=True))
    else:
        if user.is_staff:
            endpoints = Endpoint_Status.objects.all()
        else:
            endpoints = Endpoint_Status.objects.filter(
                Q(endpoint__product__authorized_users__in=[user]) |
                Q(endpoint__product__prod_type__authorized_users__in=[user]))
    return endpoints
