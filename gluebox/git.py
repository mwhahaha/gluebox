import logging
import os
import subprocess
import shutil

import gluebox.utils.git as gitutil
from gluebox.base import GlueboxCommandBase


class GlueboxGitBase(GlueboxCommandBase):
    log = logging.getLogger(__name__)

    def _get_mod_path(self, workspace, module_name):
        return os.path.abspath("{workspace}/{module}".format(
            workspace=workspace, module=module_name))

    def get_parser(self, prog_name):
        parser = super(GlueboxGitBase, self).get_parser(prog_name)
        parser.add_argument('--git-base-url', dest='git_base_url',
                            default='https://git.openstack.org/',
                            help='Base url used for cloning modules. Defaults '
                                 'to https://git.openstack.org/')
        return parser


class Checkout(GlueboxGitBase):
    """Perform module checkout to the workspace"""
    def get_parser(self, prog_name):
        parser = super(Checkout, self).get_parser(prog_name)
        parser.add_argument('-b', '--branch', default='master',
                            help='Branch to checkout. Defaults to master')
        parser.add_argument('--topic', default=None,
                            help='Topic branch to create for working on '
                                 'after checking out')
        return parser

    def take_action(self, parsed_args):

        for mod in self._get_modules(parsed_args):
            # TODO(aschultz): check if the module is already checked out
            mod_path = self._get_mod_path(parsed_args.workspace, mod)
            git_repo = "{}/{}/{}".format(parsed_args.git_base_url,
                                         parsed_args.namespace,
                                         mod)
            gitutil.checkout(git_repo=git_repo,
                             workspace=mod_path,
                             branch=parsed_args.branch,
                             topic=parsed_args.topic)

class Cleanup(GlueboxGitBase):
    """Remove module from the workspace"""
    def take_action(self, parsed_args):
        modules = self._get_modules(parsed_args)
        for mod in modules:
            mod_path = self._get_mod_path(parsed_args.workspace, mod)
            if os.path.exists(mod_path):
                self.app.stdout.write("Deleting {}\n".format(mod_path))
                shutil.rmtree(mod_path)


class Commit(GlueboxGitBase):
    """Commit changes to the module in the workspace"""
    def get_parser(self, prog_name):
        parser = super(Commit, self).get_parser(prog_name)
        parser.add_argument('-F', '--commit-message-file', default=None,
                            help='File that contains the commit message to '
                                 'use when committing. If not provided a '
                                 'generic commit message will be used.')
        return parser

    def take_action(self, parsed_args):
        self.app.stdout.write('Commit\n')
        git_message = None
        git_message_file = None
        if parsed_args.commit_message_file:
            if not os.path.exists(parsed_args.commit_message_file):
                raise Exception("missing commit message file")
            git_message_file = '-F {}'.format(
                os.path.abspath(parsed_args.commit_message_file))
        else:
            git_message = '-m "Updating module versions"'

        for mod in self._get_modules(parsed_args):
            mod_path = self._get_mod_path(parsed_args.workspace, mod)
            gitutil.commit(workspace=os.path.abspath(mod_path),
                           message=git_message,
                           message_file=git_message_file)


class PushReview(GlueboxGitBase):
    """Push the change up via git review"""
    def get_parser(self, prog_name):
        parser = super(PushReview, self).get_parser(prog_name)
        parser.add_argument('-b', '--branch', default='master',
                            help='Branch to push review to. Defaults to master')
        parser.add_argument('--topic', default='',
                            help='Topic to push as part of the review')
        return parser

    def take_action(self, parsed_args):
        self.app.stdout.write('PushReview\n')
        for mod in self._get_modules(parsed_args):
            mod_path = self._get_mod_path(parsed_args.workspace, mod)
            gitutil.review(workspace=os.path.abspath(mod_path),
                           branch=parsed_args.branch,
                           topic=parsed_args.topic)
