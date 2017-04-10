import os
import subprocess


def checkout(git_repo, workspace, branch='master',
             topic=None, git_review=None):
    print('Checkout out {} ({})...'.format(git_repo, branch))
    git_cmd = "git clone {r} -b {b} {w}".format(
        r=git_repo,
        w=workspace,
        b=branch
    )
    result = subprocess.call(git_cmd, shell=True)
    if result != 0:
        raise Exception('git clone failed')

    if topic:
        cwd = os.getcwd()
        os.chdir(os.path.abspath(workspace))
        git_cmd = 'git checkout -b {}'.format(topic)
        result = subprocess.call(git_cmd, shell=True)
        if result != 0:
            raise Exception('git checkout topic failed')
        os.chdir(cwd)

    if git_review:
        cwd = os.getcwd()
        os.chdir(os.path.abspath(workspace))
        git_cmd = 'git review -d {}'.format(git_review)
        result = subprocess.call(git_cmd, shell=True)
        if result != 0:
            raise Exception('git checkout review failed')
        os.chdir(cwd)
    return result


def commit(workspace, message=None, message_file=None, fixup=False):
    cwd = os.getcwd()
    os.chdir(workspace)

    git_add = 'git add *'
    result = subprocess.call(git_add, shell=True)
    if result != 0:
        os.chdir(cwd)
        raise Exception("git add failed")

    if fixup:
        git_opts = '--amend --no-edit'
    elif message:
        git_opts = '-m {}'.format(message)
    else:
        git_opts = '-F {}'.format(message_file)

    git_commit = 'git commit {}'.format(git_opts)
    result = subprocess.call(git_commit, shell=True)
    if result != 0:
        os.chdir(cwd)
        raise Exception("git commit failed")

    os.chdir(cwd)


def review(workspace, branch='master', topic=None):
    cwd = os.getcwd()
    os.chdir(workspace)

    git_review = 'git review {}'.format(branch)
    if topic:
        git_review = '{} -t {}'.format(git_review, topic)

    result = subprocess.call(git_review, shell=True)
    if result != 0:
        os.chdir(cwd)
        raise Exception("git review failed")
    os.chdir(cwd)


def get_hash(workspace, branch='master'):
    cwd = os.getcwd()
    os.chdir(workspace)

    git_add = ['git','rev-parse', 'origin/{}'.format(branch)]

    proc = subprocess.Popen(git_add,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    sha1, err = proc.communicate()
    result = proc.returncode

    if result != 0:
        os.chdir(cwd)
        raise Exception('git rev-parse failed {}'.format(err))
    os.chdir(cwd)
    return sha1.strip()
