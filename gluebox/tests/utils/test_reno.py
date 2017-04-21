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
from gluebox.utils.reno import RenoManager


class TestRenoManager(base.BaseTestCase):

    """Test case for reno utils."""
    def setUp(self):
        super(TestRenoManager, self).setUp()

    def test_get_current_version(self):
        manager = RenoManager('test')
        manager.reno_config = ["version = '1.0.0'", "release = '1.0.0-dev'"]
        self.assertEqual(manager.get_current_version(), '1.0.0')

    def test_get_current_release(self):
        manager = RenoManager('test')
        manager.reno_config = ["version = '1.0.0'", "release = '1.0.0-dev'"]
        self.assertEqual(manager.get_current_release(), '1.0.0-dev')

    def test_update_version_info(self):
        manager = RenoManager('test')
        manager.reno_config = ["version = '1.0.0'", "release = '1.0.0-dev'"]
        manager._parse = mock.MagicMock()
        manager._write = mock.MagicMock()
        manager.update_version_info('2.0.0', '2.0.0-dev')
        self.assertEqual(manager.reno_config, ["version = '2.0.0'",
                                               "release = '2.0.0-dev'"])
        manager._parse.assert_called_once()
        manager._write.assert_called_once()