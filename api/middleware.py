from django.conf import settings


class MethodOverrideMiddleware:
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.method != 'POST':
            return
        if settings.METHOD_OVERRIDE_HEADER not in request.META:
            return
        request.method = request.META[settings.METHOD_OVERRIDE_HEADER]