import logging
import os

from gluebox.exceptions import ModuleNotCheckedOut
from gluebox.exceptions import InvalidModuleFile
from cliff.command import Command


class GlueboxCommandBase(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GlueboxCommandBase, self).get_parser(prog_name)
        parser.add_argument('-n', '--namespace', default='openstack',
                            help='Git and puppet module namespace. Defaults to '
                                 'openstack')
        parser.add_argument('-w', '--workspace', default='workspace',
                            help='Workspace directory. Defaults to '
                                 'workspace')
        modules = parser.add_mutually_exclusive_group(required=False)
        modules.add_argument('-f', '--module-file', dest='module_file',
                             help='File that contains a list of modules to '
                                 'checkout')
        modules.add_argument('-m', '--module', nargs='*', dest='module',
                             help='Specific module to checkout')
        return parser

    def _get_modules(self, parsed_args):
        if parsed_args.module_file:
            if not os.path.exists(parsed_args.module_file):
                raise InvalidModuleFile()
            with open(parsed_args.module_file) as f:
                modules = f.read().splitlines()
        else:
            modules = ["{mod}".format(mod=i) for i in parsed_args.module]
        return modules

    def _check_module(self, workspace, module):
        mod_path = '{}/{}'.format(workspace, module)
        if not os.path.exists(mod_path):
            raise ModuleNotCheckedOut()
