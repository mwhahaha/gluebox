
import re

def gen_static_version(static_version, dev=False):
    return '{}{}'.format(
        static_version,
        '-dev' if dev else '',
    )


def _split_version(version):
    delims = '.', '-'
    pattern = '|'.join(map(re.escape, delims))
    return re.split(pattern, version)


def major_bump(version, dev=False):
    version_parts = _split_version(version)
    return '{}.0.0{}'.format(
        int(version_parts[0]) + 1,
        '-dev' if dev else ''
    )


def minor_bump(version, dev=False):
    version_parts = _split_version(version)
    return '{}.{}.0{}'.format(
        version_parts[0],
        int(version_parts[1]) + 1,
        '-dev' if dev else ''
    )


def bugfix_bump(version, dev=False):
    version_parts = _split_version(version)
    return '{}.{}.{}{}'.format(
        version_parts[0],
        version_parts[1],
        int(version_parts[2]) + 1,
        '-def' if dev else ''
    )


def dev_remove(version):
    return version.replace('-dev', '')
