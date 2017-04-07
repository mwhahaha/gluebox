import logging
import json
import re
import os

from gluebox.exceptions import MetadataJsonMissing
from gluebox.utils import version as verutil

class MetadataUpdater(object):
    log = logging.getLogger(__name__)

    def __init__(self, path, namespace):
        self.module_path = path
        self.namespace = namespace
        self.metadata = None

    def _parse(self):
        if self.metadata:
            return self.metadata

        json_file = '{}/metadata.json'.format(self.module_path)
        if not os.path.exists(json_file):
            raise MetadataJsonMissing()
        with open(json_file) as f:
            self.metadata = json.load(f)

        return self.metadata

    def _parse_ver(self, ver_string):
        pattern = "([<>=]+)?\s*([0-9.]+)(-dev)?"
        matches = re.match(pattern, ver_string)
        return matches.groups()

    def _write(self):
        json_file = '{}/metadata.json'.format(self.module_path)
        with open(json_file, 'w') as f:
            f.write(json.dumps(self.metadata, sort_keys=True, indent=4,
                    separators=(',', ': ')))

    def _fix_dependencies_major(self):
        updated_deps = []
        for dep in self.metadata['dependencies']:
            if self.namespace in dep['name']:
                (min_ver, max_ver) = dep['version_requirement'].split(' ')
                min_parts = self._parse_ver(min_ver)
                min_ver = (
                    min_parts[0],
                    verutil.major_bump(min_parts[1]),
                    min_parts[2]
                )
                max_parts = self._parse_ver(max_ver)
                max_ver = (
                    max_parts[0],
                    verutil.major_bump(max_parts[1])
                )
                dep['version_requirement'] = "{} {}".format(
                    "".join(filter(None, min_ver)),
                    "".join(filter(None, max_ver))
                )
                print("Updating {} to {}".format(
                    dep['name'], dep['version_requirement']))
            updated_deps.append(dep)
        self.metadata['dependencies'] = updated_deps


    def _fix_dependencies_minor(self):
        updated_deps = []
        for dep in self.metadata['dependencies']:
            if self.namespace in dep['name']:
                (min_ver, max_ver) = dep['version_requirement'].split(' ')
                min_parts = self._parse_ver(min_ver)
                min_ver = (
                    min_parts[0],
                    verutil.minor_bump(min_parts[1]),
                    min_parts[2]
                )
                dep['version_requirement'] = "{} {}".format(
                    "".join(filter(None, min_ver)),
                    "".join(filter(None, max_ver))
                )
                print("Updating {} to {}".format(
                    dep['name'], dep['version_requirement']))
            updated_deps.append(dep)
        self.metadata['dependencies'] = updated_deps

    def get_current_version(self):
        self._parse()
        return self.metadata['version']

    def major_bump(self, static_version=None, dev=False, skip_update_deps=False):
        self._parse()
        if static_version:
            version = verutil.gen_static_version(static_version, dev)
        else:
            version = verutil.major_bump(self.metadata['version'], dev)

        print("Version is {}".format(version))
        self.metadata['version'] = version
        if not skip_update_deps:
            self._fix_dependencies_major()
        self._write()
        return version

    def minor_bump(self, static_version=None, dev=False, skip_update_deps=False):
        self._parse()
        if static_version:
            version = verutil.gen_static_version(static_version, dev)
        else:
            version = verutil.minor_bump(self.metadata['version'], dev)
        print("Version is {}".format(version))
        self.metadata['version'] = version
        if not skip_update_deps:
            self._fix_dependencies_minor()
        self._write()
        return version

    def dev_remove(self, static_version=None):
        self._parse()
        if static_version:
            version = verutil.gen_static_version(static_version)
        else:
            version = verutil.dev_remove(self.metadata['version'])
        self.metadata['version'] = version
        self._write()
        return version
