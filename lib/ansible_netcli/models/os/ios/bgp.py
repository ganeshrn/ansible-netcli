"""
Pythonifier for BGP Ansible model
"""
from os.path import splitext

from ansible_netcli.config.loader import loadyaml

anm_ios_bgp = loadyaml(splitext(__file__)[0] + '.yaml')
