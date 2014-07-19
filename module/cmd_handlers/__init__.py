import re, os
from module.util import root_path

__all__ = []
current_path = os.path.join(root_path(), 'module/cmd_handlers')
for n in os.listdir(current_path):
    m = re.match(r'^(c_\w+)\.py$', n)
    if m and os.path.isfile(os.path.join(current_path, n)):
        __all__.append(m.group(1))
        print m.group(1)
