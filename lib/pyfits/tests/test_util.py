import os
import signal

from nose.tools import assert_equal, assert_raises

from pyfits.tests import PyfitsTestCase
from pyfits.tests.util import catch_warnings
from pyfits.util import ignore_sigint


class TestUtils(PyfitsTestCase):
    def test_ignore_sigint(self):

        @ignore_sigint
        def test():
            with catch_warnings(record=True) as w:
                pid = os.getpid()
                os.kill(pid, signal.SIGINT)
                # One more time, for good measure
                os.kill(pid, signal.SIGINT)
                assert_equal(len(w), 2)
                assert_equal(str(w[0].message),
                             'KeyboardInterrupt ignored until test is '
                             'complete!')

        assert_raises(KeyboardInterrupt, test)
