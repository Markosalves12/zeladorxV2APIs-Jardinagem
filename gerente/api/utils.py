from settings.utils import define_setting
from permissionscontrol.utils import configurate_permissions

def configurar_novo_gerente(request, model_class, obj, data):
    email = data.get('email')
    if not email:
        return

    define_setting(request=request, model_class=model_class, email=email)
    configurate_permissions(request=request, model_class=model_class, email=email)