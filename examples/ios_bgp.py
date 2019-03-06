
from os.path import splitext
from yaml import load

from ansible_netcli.models.os.ios.bgp import anm_ios_bgp
from ansible_netcli.config.translator import ConfigTranslator


def main():
    with open(splitext(__file__)[0] + '_config.yaml') as fp:
        params = load(fp)

    cfg = ConfigTranslator(anm_ios_bgp)

    #print("IOS BGP SPEC: %s\n" % cfg.options)
    #print("Input params: %s\n" % params)

    commands = cfg.render_commands(params[0]['ios_bgp'])
    print("Commands generated:\n\n%s" % "\n".join(commands))


if __name__ == '__main__':
    main()
