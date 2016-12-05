from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import pytest

from flexget.task import TaskAbort


class TestQualityPriority(object):
    config = """
        tasks:
          test_reorder_quality:
            mock:
              - {title: 'Some Show S01E01 WEBRip'}
              - {title: 'Some Show S01E01 HDTV'}
            reorder_quality:
              webrip:
                above: hdtv
            series:
              - Some Show:
                  identified_by: ep
          test_normal_quality_priority:
            mock:
              - {title: 'Some Show S01E02 WEBRip'}
              - {title: 'Some Show S01E02 HDTV'}
            series:
              - Some Show:
                  identified_by: ep
          test_invalid_reorder_quality:
            reorder_quality:
              h264:
                above: hdtv
    """

    def test_reorder_quality(self, execute_task):
        task = execute_task('test_reorder_quality')

        assert task.find_entry('accepted', title='Some Show S01E01 WEBRip'), 'WEBRip should have been accepted'

        task = execute_task('test_normal_quality_priority')
        assert task.find_entry('accepted', title='Some Show S01E02 HDTV'), 'HDTV should have been accepted'

    def test_invalid_reorder_quality(self, execute_task):
        with pytest.raises(TaskAbort) as e:
            execute_task('test_invalid_reorder_quality')
        assert e.value.reason == 'h264=codec and hdtv=source do not have the same quality type'
