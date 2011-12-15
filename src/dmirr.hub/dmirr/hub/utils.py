
from django.conf import settings
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403

# shortcut
ok = permission_required_or_403
Http403 = HttpResponseForbidden()
