from functools import wraps
from django.core.exceptions import PermissionDenied


def perfil_required(*perfis):
    """
    Decorator que restringe uma view a usuários com determinado(s) perfil(is).

    Uso:
        @perfil_required('ADMIN', 'GESTOR')
        def minha_view(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if user.is_superuser or getattr(user, 'perfil', None) in perfis:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped
    return decorator
