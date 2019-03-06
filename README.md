# ABOUT

The repo is under active development.  If you take a clone, you are getting the latest,
and perhaps not entirely stable code.

ansible-netcli is a tool and python library that provides interfaces to parse
the Ansible Network model shipped with this library and input configuration to generate device specific commands.
It also provides interface to convert Network text configuration into JSON format defined by the Ansible
Network model structure.
It can be used as a standalone tool, or as a Python module that can be imported.
The goal is to provide a stable and consistent interface abstraction to Ansible Network resource modules.

# INSTALLATION

## PIP

Installing from Git is also supported (OS must have git installed).

	To install the latest DEVEL code
	pip install git+https://github.com/ganeshrn/ansible-netcli.git
	-or-
	To install a specific version, branch, tag, etc.
	pip install git+https://github.com/ganeshrn/ansible-netcli.git@<branch,tag,commit>

## Upgrade

Upgrading has the same requirements as installation and has the same format with the addition of -UPGRADE

	pip install -U git+https://github.com/ganeshrn/ansible-netcli.git

## Developer Guide

- [Ansible Network Model](https://github.com/ganeshrn/ansible-netcli/blob/devel/docs/anm/README.md)
- [How to use](https://github.com/ganeshrn/ansible-netcli/blob/devel/docs/user_guide/README.md)


# LICENSE

Apache 2.0


# CONTRIBUTORS

Ansible Network Community (ansible-network)
