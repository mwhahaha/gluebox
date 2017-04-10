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
import gluebox.utils.git as git


class TestGit(base.BaseTestCase):

    """Test cases for git utils"""
    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_checkout(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value=0

        git.checkout('https://blah/', '/test', 'foo')

        call_mock.assert_called_once_with('git clone https://blah/ -b foo '
                                          '/test', shell=True)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_checkout_with_topic(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value=0

        git.checkout('https://blah/', '/test', topic='test-topic')

        calls = [
            mock.call('git clone https://blah/ -b master /test', shell=True),
            mock.call('git checkout -b test-topic', shell=True),
        ]

        call_mock.assert_has_calls(calls)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_checkout_with_review(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value=0

        git.checkout('https://blah/', '/test', git_review='12345')

        calls = [
            mock.call('git clone https://blah/ -b master /test', shell=True),
            mock.call('git review -d 12345', shell=True),
        ]

        call_mock.assert_has_calls(calls)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_commit(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value=0

        git.commit('/test', message='foo')

        calls = [
            mock.call('git add *', shell=True),
            mock.call('git commit -m "foo"',  shell=True),
        ]

        call_mock.assert_has_calls(calls)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_commit_message_file(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value=0

        git.commit('/test', message_file='/file.txt')

        calls = [
            mock.call('git add *', shell=True),
            mock.call('git commit -F /file.txt', shell=True),
        ]

        call_mock.assert_has_calls(calls)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_commit_fixup(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value = 0

        git.commit('/test', fixup=True)

        calls = [
            mock.call('git add *', shell=True),
            mock.call('git commit --amend --no-edit', shell=True),
        ]

        call_mock.assert_has_calls(calls)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_review(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value = 0

        git.review('/test')

        call_mock.assert_called_once_with('git review master', shell=True)

    @mock.patch('subprocess.call')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_review_with_topic(self, getcwd_mock, chdir_mock, call_mock):
        getcwd_mock.return_value = '/tmp'
        call_mock.return_value = 0

        git.review('/test', topic='foo')

        call_mock.assert_called_once_with('git review master -t foo',
                                          shell=True)

    @mock.patch('subprocess.Popen')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_get_hash(self, getcwd_mock, chdir_mock, popen_mock):
        getcwd_mock.return_value = '/tmp'
        proc_mock = mock.MagicMock(returncode=0)
        proc_mock.communicate.side_effect = [('12345',None)]
        popen_mock.return_value = proc_mock

        val = git.get_hash('/test')

        getcwd_mock.assert_called_once()
        popen_mock.assert_called_once_with(['git', 'rev-parse', 'origin/master'],
                                           stderr=-1,
                                           stdout=-1)
        self.assertEqual(val, '12345')

    @mock.patch('subprocess.Popen')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    def test_get_hash_parse_failed(self, getcwd_mock, chdir_mock, popen_mock):
        getcwd_mock.return_value = '/tmp'
        proc_mock = mock.MagicMock(returncode=1)
        proc_mock.communicate.side_effect = [('12345', None)]
        popen_mock.return_value = proc_mock
        self.assertRaises(Exception, git.get_hash, '/test')
