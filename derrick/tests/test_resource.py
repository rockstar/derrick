'''Tests for derrick.resource.'''
import os

from twisted.trial import unittest

from derrick.resource import DerrickRootResource


class DerrickRootResourceTest(unittest.TestCase):
    '''Test derrick.resource.DerrickRootResource.'''

    def test__is_safe(self):
        '''Files inside root are okay.'''
        resource = DerrickRootResource()
        self.assertTrue(resource._is_safe('safefile'))

    def test__is_safe_with_directory(self):
        '''Files inside directories inside root are okay.'''
        resource = DerrickRootResource()
        self.assertTrue(resource._is_safe('foo/safefile'))

    def test__is_safe_double_dots(self):
        '''Double dots are allowed if they don't leak.'''
        resource = DerrickRootResource()
        self.assertTrue(resource._is_safe('foo/../safefile'))

    def test__is_safe_double_dots_leak(self):
        '''Double dots aren't allowed if they leak.'''
        resource = DerrickRootResource()
        self.assertFalse(resource._is_safe('../safefile'))

    def test__is_safe_absolute_not_safe(self):
        '''Absolute paths that leak also aren't allowed.'''
        resource = DerrickRootResource()
        self.assertFalse(resource._is_safe('/etc/passwd'))
