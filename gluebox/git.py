import logging
import os
import subprocess
import shutil

from gluebox.base import GlueboxCommandBase


class GlueboxGitBase(GlueboxCommandBase):
    log = logging.getLogger(__name__)

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
        cwd = os.getcwd()
        for mod in self._get_modules(parsed_args):
            # TODO(aschultz): check if the module is already checked out
            mod_path = "{workspace}/{module}".format(
                workspace=parsed_args.workspace, module=mod)
            print('Checkout out {} ({})...'.format(mod, parsed_args.branch))
            git_cmd = "git clone {u}/{n}/{m} -b {b} {w}/{m}".format(
                u=parsed_args.git_base_url,
                n=parsed_args.namespace,
                w=parsed_args.workspace,
                m=mod,
                b=parsed_args.branch
            )
            #self.app.stdout.write(git_cmd)
            result = subprocess.call(git_cmd, shell=True)
            if result != 0:
                raise Exception("git clone failed")
            if parsed_args.topic:
                os.chdir(os.path.abspath(mod_path))
                git_cmd = 'git checkout -b {}'.format(parsed_args.topic)
                result = subprocess.call(git_cmd, shell=True)
                if result != 0:
                    raise Exception("git checkout topic failed")
                os.chdir(cwd)




class Cleanup(GlueboxGitBase):
    """Remove module from the workspace"""
    def take_action(self, parsed_args):
        modules = self._get_modules(parsed_args)
        for mod in modules:
            mod_path = "{workspace}/{module}".format(
                workspace=parsed_args.workspace, module=mod)
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
        cwd = os.getcwd()
        if parsed_args.commit_message_file:
            if not os.path.exists(parsed_args.commit_message_file):
                raise Exception("missing commit message file")
            git_message = '-F {}'.format(
                os.path.abspath(parsed_args.commit_message_file))
        else:
            git_message = '-m "Updating module versions"'
        for mod in self._get_modules(parsed_args):
            mod_path = "{workspace}/{module}".format(
                workspace=parsed_args.workspace, module=mod)
            os.chdir(os.path.abspath(mod_path))

            git_add = 'git add *'
            result = subprocess.call(git_add, shell=True)
            if result != 0:
                os.chdir(cwd)
                raise Exception("git add failed")

            git_commit = "git commit {}".format(git_message)
            result = subprocess.call(git_commit, shell=True)
            if result != 0:
                os.chdir(cwd)
                raise Exception("git commit failed")

            os.chdir(cwd)


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
        cwd = os.getcwd()
        for mod in self._get_modules(parsed_args):
            mod_path = "{workspace}/{module}".format(
                workspace=parsed_args.workspace, module=mod)
            os.chdir(os.path.abspath(mod_path))

            git_add = 'git review {}'.format(parsed_args.branch)
            if parsed_args.topic:
                git_add = '{} -t {}'.format(git_add, parsed_args.topic)

            print(git_add)
            result = subprocess.call(git_add, shell=True)
            if result != 0:
                os.chdir(cwd)
                raise Exception("git review failed")
            os.chdir(cwd)
