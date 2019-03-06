# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from copy import deepcopy
from jinja2 import Template, StrictUndefined
from jinja2.exceptions import UndefinedError

from ansible_netcli.common.utils import to_list
from six import iteritems


class ConfigTranslator(object):
    def __init__(self, spec):
        self.cmd_index_map = {}
        self.commands = []
        self.unresolved_command = {}
        self.spec = spec

    @property
    def anm_version(self):
        return self.spec['anm_version']

    @property
    def options(self):
        return self.spec['anm_spec']['options']

    def render_commands(self, params):
        self.operation = params['operation']
        self.configs = params['config']
        self.commands = []
        self.unresolved_command = {}

        for config in to_list(self.configs):
            for k, v in iteritems(self.options):
                variables = {}
                if config.get(k):
                    option_type = v.get('type')
                    option_elements = v.get('elements')
                    if v.get('options'):
                        if option_type == 'list' and option_elements == 'dict':
                            cmd = self._handle_list(k, v, config[k])
                        elif option_type == 'dict':
                            cmd = self._handle_container(k, v, config[k])
                    elif option_type == 'list' and option_elements != 'dict':
                        cmd = self._handle_leaf_list(k, v, config[k])
                    else:
                        variables.update({k: config[k]})
                        cmd = self._handle_leaf(k, v, variables)
                    if cmd:
                        self.commands.extend(cmd)

        return self.commands

    def _handle_list(self, param, value, configs):
        list_command = []
        metadata = value['metadata']
        cmd_obj = metadata['command']
        entry_template = cmd_obj.get('entry', [])
        exit_template = cmd_obj.get('exit', [])

        if entry_template:
            command = Template(entry_template, undefined=StrictUndefined).render(self.cmd_index_map)
            list_command.append(" " * cmd_obj.get('indent', 0) + command)

        child_command = []
        for config in configs:
            for k, v in iteritems(value.get('options')):
                variables = {}
                if config.get(k):
                    option_type = v.get('type')
                    option_elements = v.get('elements')
                    if v.get('options'):
                        if option_type == 'list' and option_elements == 'dict':
                            cmd = self._handle_list(k, v, config[k])
                        elif option_type == 'dict':
                            cmd = self._handle_container(k, v, config[k])
                    elif option_type == 'list' and option_elements != 'dict':
                        cmd = self._handle_leaf_list(k, v, config[k])
                    else:
                        variables.update({k: config[k]})
                        cmd = self._handle_leaf(k, v, variables)
                    if cmd:
                        child_command.extend(cmd)

            combine = metadata.get('combine')
            indent = metadata.get('indent', 0)
            if combine:
                for item in to_list(combine):
                    command = Template(item, undefined=StrictUndefined).render(self.cmd_index_map)
                    list_command.append(" " * indent + command)

        list_command.extend(child_command)
        if exit_template:
            command = Template(exit_template, undefined=StrictUndefined).render(self.cmd_index_map)
            list_command.append(" " * indent + command)

        return list_command

    def _handle_container(self, param, value, config):
        container_command = []
        metadata = value['metadata']
        cmd_obj = metadata['command']
        entry_template = cmd_obj.get('entry', [])
        exit_template = cmd_obj.get('exit', [])

        if entry_template:
            command = Template(entry_template, undefined=StrictUndefined).render(self.cmd_index_map)
            container_command.append(" " * cmd_obj.get('indent', 0) + command)

        child_command = []
        for k, v in iteritems(value.get('options')):
            variables = {}
            if config.get(k):
                option_type = v.get('type')
                option_elements = v.get('elements')
                if v.get('options'):
                    if option_type == 'list' and option_elements == 'dict':
                        cmd = self._handle_list(k, v, config[k])
                    elif option_type == 'dict':
                        cmd = self._handle_container(k, v, config[k])
                elif option_type == 'list' and option_elements != 'dict':
                    cmd = self._handle_leaf_list(k, v, config[k])
                else:
                    variables.update({k: config[k]})
                    cmd = self._handle_leaf(k, v, variables)
                if cmd:
                    child_command.extend(cmd)

        combine = metadata.get('combine')
        indent = metadata.get('indent', 0)
        if combine:
            for item in to_list(combine):
                command = Template(item, undefined=StrictUndefined).render(self.cmd_index_map)
                container_command.append(" " * indent + command)

        container_command.extend(child_command)
        if exit_template:
            command = Template(exit_template, undefined=StrictUndefined).render(self.cmd_index_map)
            container_command.append(" " * indent + command)

        return container_command

    def _handle_leaf_list(self, param, value, config):
        return []

    def _handle_leaf(self, param, value, config):

        variables = deepcopy(config)
        variables.update(self.cmd_index_map)

        metadata = value['metadata']

        # TODO: Add support for forward looking reference
        # try:
        leaf_command = self._build_command(metadata, param, variables)
        # except UndefinedError:
        #    self.unresolved_command.update({param: value})
        return leaf_command

    def _build_command(self, metadata, param, variables):
        leaf_command = []
        cmd_obj = metadata['command']
        indent = metadata.get('indent', 0)
        index = str(cmd_obj['index'])

        cmd_template = self._get_command_template(cmd_obj, param)

        for cmd in cmd_template:
            command = Template(cmd, undefined=StrictUndefined).render(variables)
            if not cmd_obj.get('cmdref'):
                leaf_command.append(" " * indent + command)
            self.cmd_index_map["__" + index] = command

        return leaf_command

    def _get_command_template(self, cmd_obj, param):

        delete_template = cmd_obj.get('delete', [])
        merge_template = cmd_obj.get('merge', [])
        override_template = cmd_obj.get('override', [])
        replace_template = cmd_obj.get('replace', [])

        if self.operation == "delete":
            cmd_template = delete_template
        elif self.operation == "merge":
            cmd_template = merge_template
        elif self.operation == "override":
            if override_template:
                cmd_template = override_template
            else:
                cmd_template = merge_template
        elif self.operation == "replace":
            if replace_template:
                cmd_template = replace_template
            else:
                cmd_template = merge_template
        else:
            raise ValueError("Invalid value for operation %s for option %s" % (self.operation, param))

        return to_list(cmd_template)
