# Overview

`vartoml` allows using variables in TOML config files. It uses the `toml` package.

# Acknowledgent

The idea how to tackle the problem of variable interpolation was taken
from the `envtoml` package which is at https://github.com/mrshu/envtoml .

# Variable names in TOML file

Variables are specified this way: `${section:variable}`. Deeper nested 
variables are not supported.

# Example

```toml
[default]

basedir = "/myproject"
bindir = "${default:basedir}/bin"
datadir = "${default:basedir}/data"


[other.dirs]

logdir = "${default:datadir}/logs"
```
