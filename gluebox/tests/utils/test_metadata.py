#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from oslotest import base
from gluebox.utils.metadata import MetadataManager


class TestMetadata(base.BaseTestCase):

    """Test case for metadata utils."""
    def setUp(self):
        super(TestMetadata, self).setUp()

    def _dummy_metadata(self):
        data = {
            u'issues_url': u'https://bugs.launchpad.net/puppet-aodh',
            u'requirements': [
                {u'name': u'pe', u'version_requirement': u'4.x'},
                {u'name': u'puppet', u'version_requirement': u'4.x'}
            ],
            u'name': u'openstack-aodh',
            u'license': u'Apache-2.0',
            u'author': u'OpenStack Contributors',
            u'project_page': u'https://launchpad.net/puppet-aodh',
            u'operatingsystem_support': [
                {u'operatingsystemrelease': [u'8'],
                 u'operatingsystem': u'Debian'},
                {u'operatingsystemrelease': [u'24'],
                 u'operatingsystem': u'Fedora'},
                {u'operatingsystemrelease': [u'7'],
                 u'operatingsystem': u'RedHat'},
                {u'operatingsystemrelease': [u'16.04'],
                 u'operatingsystem': u'Ubuntu'}
            ],
            u'summary': u'Puppet module for OpenStack Aodh',
            u'source': u'git://github.com/openstack/puppet-aodh.git',
            u'dependencies': [
                {u'name': u'puppetlabs/inifile',
                 u'version_requirement': u'>=1.0.0 <2.0.0'},
                {u'name': u'puppetlabs/stdlib',
                 u'version_requirement': u'>= 4.2.0 <5.0.0'},
                {u'name': u'openstack/keystone',
                 u'version_requirement': u'>=11.0.0 <12.0.0'},
                {u'name': u'openstack/openstacklib',
                 u'version_requirement': u'>=11.0.0 <12.0.0'},
                {u'name': u'openstack/oslo',
                 u'version_requirement': u'>=11.0.0 <12.0.0'}
            ],
            u'version': u'11.0.0',
            u'description': u'Installs and configures OpenStack Aodh.'
        }
        return data

    def test_get_current_version(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        self.assertEqual(manager.get_current_version(), '11.0.0')

    def test_fix_dependencies_major(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._fix_dependencies_major()
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=12.0.0 <13.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=12.0.0 <13.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=12.0.0 <13.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)

    def test_fix_dependencies_minor(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._fix_dependencies_minor()
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.1.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.1.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.1.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)

    def test_major_bump(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.major_bump()
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=12.0.0 <13.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=12.0.0 <13.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=12.0.0 <13.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '12.0.0')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_major_bump_with_static_dev_version(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.major_bump('12.0.1', True)
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=12.0.0 <13.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=12.0.0 <13.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=12.0.0 <13.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '12.0.1-dev')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_major_bump_skip_deps(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.major_bump(skip_update_deps=True)
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.0.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '12.0.0')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_minor_bump(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.minor_bump()
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.1.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.1.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.1.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '11.1.0')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_minor_bump_with_static_dev_version(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.minor_bump('11.1.1', True)
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.1.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.1.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.1.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '11.1.1-dev')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_minor_bump_skip_deps(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.minor_bump(skip_update_deps=True)
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.0.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '11.1.0')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_dev_remove(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager.metadata['version'] = '11.0.0-dev'
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.dev_remove()
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.0.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '11.0.0')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()

    def test_dev_remove_with_static_version(self):
        manager = MetadataManager('puppet-aodh', 'openstack')
        manager.metadata = self._dummy_metadata()
        manager.metadata['version'] = '11.0.0-dev'
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.dev_remove('11.0.0-abc')
        updated_deps = [
            {u'name': u'puppetlabs/inifile',
             u'version_requirement': u'>=1.0.0 <2.0.0'},
            {u'name': u'puppetlabs/stdlib',
             u'version_requirement': u'>= 4.2.0 <5.0.0'},
            {u'name': u'openstack/keystone',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/openstacklib',
             u'version_requirement': u'>=11.0.0 <12.0.0'},
            {u'name': u'openstack/oslo',
             u'version_requirement': u'>=11.0.0 <12.0.0'}
        ]
        self.assertEqual(manager.metadata['dependencies'], updated_deps)
        self.assertEqual(manager.metadata['version'], '11.0.0-abc')
        manager._parse.assert_called_once()
        manager._write.assert_called_once()