__version__ = "0.1.0-alpha"

import toml
import os
import re


RE_ENV_VAR = r"\$\{([a-zA-Z0-9_]+:[a-zA-Z0-9_]+)\}"


class VarToml:
    def __init__(self):
        self.decoder = toml.TomlDecoder()

    def load(self, *args, **kwargs):
        self.data = toml.load(*args, **kwargs)
        self.process(self.data)

    def loads(self, *args, **kwargs):
        self.data = toml.loads(*args, **kwargs)
        self.process(self.data)

    def var_replace(self, x):
        toml_var = x.groups()[0]
        (section, item) = toml_var.split(":")
        return str(self.data[section][item])

    def get(self, *args):
        gotten = self.data
        for arg in args:
            gotten = gotten[arg]
        return gotten

    def show(self):
        return self.data

    def process(self, item):
        iter_ = None
        if isinstance(item, dict):
            iter_ = item.items()
        elif isinstance(item, list):
            iter_ = enumerate(item)

        for i, val in iter_:
            if isinstance(val, (dict, list)):
                self.process(val)
            elif isinstance(val, str):
                if re.search(RE_ENV_VAR, val):
                    r = re.sub(RE_ENV_VAR, self.var_replace, val)

                    # Try to first load the value from the environment variable
                    # (i.e. make what seems like a float a float, what seems like a
                    # boolean a bool and so on). If that fails, fail back to
                    # string.
                    try:
                        item[i], _ = self.decoder.load_value(r)
                        continue
                    except ValueError:
                        pass

                    item[i], _ = self.decoder.load_value('"{}"'.format(r))
