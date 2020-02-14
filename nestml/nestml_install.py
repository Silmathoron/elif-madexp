import os

from pynestml.frontend.pynestml_frontend import to_nest, install_nest

# folder

home   = os.path.expanduser("~")
folder = os.path.dirname(__file__)
root   = os.path.abspath(folder if folder else ".")
target = root + "/build"

# build

to_nest(logging_level='ERROR', input_path=root, target_path=target,
        module_name="energy_module", dev=True)

# install

import nest

nest_file = nest.__file__

pos = nest_file.find("/lib")

install_nest(target, nest_file[:pos])
