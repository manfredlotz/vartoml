#!/usr/bin/env python3


#
# A demo script to show how to use the `vartoml` package
#

from vartoml import VarToml

vtoml = VarToml()

def demo1():
    """A simple TOML document without any variables

        This works the same as when using the `toml` package
    """

    tomls_str ="""
    [default]

    h = "/home"

    """
    vtoml.loads(tomls_str)
    print(vtoml.get('default', 'h'))

def demo2():
    """A simple TOML document using variables """

    tomls_str = """

    [default]

    h = "/home"
    m = "${default:h}/manfred"
    b = "${default:m}/bin"

    [other]

    server = "${default:b}/server"
    """

    vtoml.loads(tomls_str)
    print(vtoml.get('other', 'server'))



def main():
    demo1()
    demo2()


if __name__ == "__main__":
    main()

