import logging
import re
import argparse

from gluebox.base import GlueboxCommandBase
from gluebox.utils.metadata import MetadataUpdater


class GlueboxVersionBase(GlueboxCommandBase):
    log = logging.getLogger(__name__)

    def _static_version(self, str):
        try:
            return re.match("^[0-9]+\.[0-9]+\.[0-9]+$", str).group(0)
        except:
            raise argparse.ArgumentTypeError(
                "String '%s' does not match required format" % (str,))

    def get_parser(self, prog_name):
        parser = super(GlueboxVersionBase, self).get_parser(prog_name)
        parser.add_argument('--dev', action='store_true', default=False,
                            help='Append -dev to the version number when '
                                 'bumping versions.')
        parser.add_argument('--static-version', default=None,
                            type=self._static_version,
                            help='Specify a specific version to use rather '
                                 'than figuring it out from the previous '
                                 'defined version in the module. Format is '
                                 '"X.Y.Z". Use --dev if you wish to force '
                                 '"X.Y.Z-dev".')
        parser.add_argument('--skip-update-deps', action='store_true',
                            default=False,
                            help='Update the metadata dependencies in the '
                                 'namespace. Only affects minorbump and '
                                 'majorbump')
        return parser


class MajorBump(GlueboxVersionBase):
    """Perform a major version bump"""
    def take_action(self, parsed_args):
        self.app.stdout.write('Major\n')
        for mod in self._get_modules(parsed_args):
            self.app.stdout.write('MajorBump {} ... '.format(mod))
            self._check_module(parsed_args.workspace, mod)
            path = '{}/{}'.format(parsed_args.workspace, mod)
            updater = MetadataUpdater(path, parsed_args.namespace)
            v = updater.major_bump(static_version=parsed_args.static_version,
                                   dev=parsed_args.dev,
                                   skip_update_deps=parsed_args.skip_update_deps)
            self.app.stdout.write('{}\n'.format(v))




class MinorBump(GlueboxVersionBase):
    """Perform a minor version bump"""
    def take_action(self, parsed_args):
        for mod in self._get_modules(parsed_args):
            self.app.stdout.write('MinorBump {} ... '.format(mod))
            self._check_module(parsed_args.workspace, mod)
            path = '{}/{}'.format(parsed_args.workspace, mod)
            updater = MetadataUpdater(path, parsed_args.namespace)
            v= updater.minor_bump(static_version=parsed_args.static_version,
                                  dev=parsed_args.dev,
                                  skip_update_deps=parsed_args.skip_update_deps)
            self.app.stdout.write('{}\n'.format(v))

class DevBump(GlueboxVersionBase):
    """Remove -dev from existing version"""
    def take_action(self, parsed_args):
        for mod in self._get_modules(parsed_args):
            self.app.stdout.write('DevBump {} ... '.format(mod))
            self._check_module(parsed_args.workspace, mod)
            path = '{}/{}'.format(parsed_args.workspace, mod)
            updater = MetadataUpdater(path, parsed_args.namespace)
            v = updater.dev_remove(static_version=parsed_args.static_version)
            self.app.stdout.write('{}\n'.format(v))