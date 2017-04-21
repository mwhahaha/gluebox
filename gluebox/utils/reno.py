import logging
import re
import os

from gluebox.exceptions import RenoConfMissing

class RenoManager(object):
    log = logging.getLogger(__name__)

    def __init__(self, path):
        self.module_path = path
        self.reno_config = None

    def _parse(self):
        if self.reno_config:
            return self.reno_config

        conf_file = '{}/releasenotes/source/conf.py'.format(
            self.module_path)
        self.log.debug("reading {}".format(conf_file))

        if not os.path.exists(conf_file):
            raise RenoConfMissing()
        with open(conf_file, 'r') as f:
            self.reno_config = f.read().splitlines()

        return self.reno_config

    def _write(self):
        conf_file = '{}/releasenotes/source/conf.py'.format(
            self.module_path)
        self.log.debug("writing to {}".format(conf_file))

        if not os.path.exists(conf_file):
            raise RenoConfMissing()
        with open(conf_file, 'w') as f:
            f.write("\n".join(self.reno_config))
            # it's python so we should have a trailing \n
            f.write("\n")

        return self.reno_config

    def _parse_ver(self, ver_string):
        pattern = "(\w*)\s*([<>=]+)?\s*'([0-9.]+(-dev)?)'"
        matches = re.match(pattern, ver_string)
        if not matches:
            return None
        return matches.groups()

    def _parse_version_line(self, line):
        ver_parts = self._parse_ver(line)
        if not ver_parts:
            return None
        return ver_parts[2]

    def get_current_version(self):
        self._parse()
        ver_lines = [item for item in self.reno_config
                     if item.startswith('version ')]
        if not ver_lines:
            return None
        return self._parse_version_line(ver_lines[0])

    def get_current_release(self):
        self._parse()
        rel_lines = [item for item in self.reno_config
                     if item.startswith('release ')]
        if not rel_lines:
            return None
        return self._parse_version_line(rel_lines[0])

    def update_version_info(self, version, release):
        self._parse()
        self.log.debug("Updating version...")
        pos = [i for i, v in enumerate(self.reno_config)
               if v.startswith('version ')]
        self.reno_config[pos[0]] = "version = '{}'".format(version)
        self.log.debug("version is... {}".format(self.reno_config[pos[0]]))
        pos = [i for i, v in enumerate(self.reno_config)
               if v.startswith('release ')]
        self.reno_config[pos[0]] = "release = '{}'".format(release)
        self.log.debug("release is... {}".format(self.reno_config[pos[0]]))
        self._write()

