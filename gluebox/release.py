import logging
import os
import shutil

from gluebox.base import GlueboxCommandBase
from gluebox.utils.metadata import MetadataUpdater
import gluebox.utils.git as gitutils

RELEASE_REPO = 'https://git.openstack.org/openstack/releases'

class GlueboxReleaseBase(GlueboxCommandBase):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GlueboxReleaseBase, self).get_parser(prog_name)
        parser.add_argument('--release-repo', default=RELEASE_REPO,
                            help='Git repository for the OpenStack releases. '
                                 'Defaults to {}'.format(RELEASE_REPO))
        return parser


class CleanupRelease(GlueboxReleaseBase):
    """Cleanup the releases workspace"""
    def take_action(self, parsed_args):
        workspace = os.path.abspath("{}/{}".format(
            parsed_args.workspace, 'releases'))
        if os.path.exists(workspace):
            self.app.stdout.write("Deleting {}\n".format(workspace))
            shutil.rmtree(workspace)


class NewRelease(GlueboxReleaseBase):
    """Create a new release entry for a given release"""
    def get_parser(self, prog_name):
        parser = super(NewRelease, self).get_parser(prog_name)
        parser.add_argument('release',
                            help='OpenStack release version to work with. '
                                 'Examples: pike or ocata')
        parser.add_argument('--branch', default='master',
                            help='Branch to release from. Defaults to master')
        return parser

    def take_action(self, parsed_args):
        workspace = os.path.abspath("{}/{}".format(
            parsed_args.workspace, 'releases'))
        if not os.path.exists(workspace):
            gitutils.checkout(git_repo=parsed_args.release_repo,
                              workspace=workspace)
        else:
            self.log.warning('Reusing checked out release repo.')
        hashes = {}
        for mod in self._get_modules(parsed_args):
            path = os.path.abspath('{}/{}'.format(parsed_args.workspace, mod))
            metadata = MetadataUpdater(path, parsed_args.namespace)
            info = {'sha1': gitutils.get_hash(path, parsed_args.branch),
                    'version': metadata.get_current_version() }
            hashes[mod] = info

        print(hashes)
