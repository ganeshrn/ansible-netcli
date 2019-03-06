# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from copy import deepcopy
from collections import OrderedDict
from yaml import load
from six import iteritems

VALID_SPEC_KEYS = ('anm_version', 'anm_spec')


class Loader(object):
    def __init__(self, path):
        with open(path) as fp:
            spec = load(fp)

        self.spec = spec
        self.ordered_spec = OrderedDict()
        for item in spec:
            if item not in VALID_SPEC_KEYS:
                raise ValueError("Invalid key '%s' in spec. Valid values are %s." % (item, ', '.join(VALID_SPEC_KEYS)))
            self.ordered_spec[item] = deepcopy(spec[item])

    def load(self):
        options = self.spec['anm_spec']['options']
        self.ordered_spec['anm_spec']['options'] = self._handle_options(options)
        return self.ordered_spec

    def _handle_options(self, options, index=0):
        ordered_options = OrderedDict()

        for count in range(len(options) + 2):
            for k, v in iteritems(options):
                try:
                    option_index = str(v['metadata']['command']['index'])
                except IndexError:
                    raise IndexError("Invalid option index %s for option %s with contents %s" % (option_index, k, v))

                if option_index.split('_')[index] == str(count + 1):
                    ordered_options[k] = v
                    if v.get('options'):
                        v['options'] = self._handle_options(v['options'], index + 1)
                    break
        return ordered_options


def loadyaml(path):
    return Loader(path).load()
