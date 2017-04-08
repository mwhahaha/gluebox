import logging
import os
import shutil
import yaml

from gluebox.base import GlueboxCommandBase
from gluebox.utils.metadata import MetadataManager
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
        parser.add_argument('--create-stable', action='store_true',
                            default=False,
                            help='Create a stable branch entry for the version'
                                 'being released.')
        return parser

    def take_action(self, parsed_args):
        workspace = os.path.abspath("{}/{}".format(
            parsed_args.workspace, 'releases'))
        if not os.path.exists(workspace):
            gitutils.checkout(git_repo=parsed_args.release_repo,
                              workspace=workspace)
        else:
            self.log.warning('Reusing checked out release repo.')
        for mod in self._get_modules(parsed_args):
            path = os.path.abspath('{}/{}'.format(parsed_args.workspace, mod))
            metadata = MetadataManager(path, parsed_args.namespace)
            info = {'version': str(metadata.get_current_version()),
                    'projects': [
                        {'repo': '{}/{}'.format(parsed_args.namespace, mod),
                         'hash': gitutils.get_hash(path, parsed_args.branch)}
                    ]}
            release_file = '{}/deliverables/{}/{}.yaml'.format(
                workspace, parsed_args.release.lower(), mod)
            if not os.path.exists(release_file):
                raise Exception('Release file {} does not exist'.format(
                    release_file))
            with open(release_file, 'r') as rfile:
                data = yaml.load(rfile)

            if 'releases' not in data:
                data['releases'] = []
            elif any(v['version'] == info['version'] for v in data['releases']):
                raise Exception('Version already defined in release')

            data['releases'].append(info)

            if parsed_args.create_stable:
                stable_branch = 'stable/{}'.format(parsed_args.release)
                branch_data = {'name': stable_branch,
                               'location': info['version']}
                if 'branches' not in data:
                    data['branches'] = []
                elif any(v['name'] == stable_branch for v in data['branches']):
                    raise Exception('Stable branch already defined in release')

                data['branches'].append(branch_data)

            with open(release_file, 'w') as rfile:
                yaml.dump(data, rfile, explicit_start=True,
                          default_flow_style=False)


class UpdateRelease(GlueboxReleaseBase):
    """Update a new release entry from an existing review"""
    def get_parser(self, prog_name):
        parser = super(UpdateRelease, self).get_parser(prog_name)
        parser.add_argument('release',
                            help='OpenStack release version to work with. '
                                 'Examples: pike or ocata')
        parser.add_argument('--branch', default='master',
                            help='Branch to release from. Defaults to master')
        parser.add_argument('--create-stable', action='store_true',
                            default=False,
                            help='Create a stable branch entry for the version'
                                 'being released.')
        parser.add_argument('review',
                            help='Gerrit review ID for the existing release '
                                 'update')
        return parser

    def take_action(self, parsed_args):
        pass