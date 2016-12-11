#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest

from sugarloaf import tasks
from sugarloaf.models import Trail, TrailStatus, Lift, LiftStatus, DailyReport, SnowReporter

from .shared import my_vcr, REPORT_VCR_DIR


def check_trails_lifts():
    """ Check that there are a reasonable number of lift and trail reports """
    assert Trail.query.count() >= 150
    assert TrailStatus.query.count() >= 150

    assert Trail.query.filter_by(name='Upper Gondola Line').first() is not None
    assert Trail.query.filter_by(name='Misery Whip').first() is not None

    assert Lift.query.count() >= 13
    assert LiftStatus.query.count() >= 13

    assert Lift.query.filter_by(name='SuperQuad').first() is not None
    assert Lift.query.filter_by(name='King Pine').first() is not None


@pytest.mark.usefixtures('testapp')
class TestTasks:
    def test_update_trails_lifts(self, testapp):
        """ Test that the current trail and lift data can be brought in """
        
        with my_vcr.use_cassette(REPORT_VCR_DIR):
            tasks.update_trails_lifts()
        
        check_trails_lifts()
    
    def test_update_report(self, testapp):
        """ Test that the daily report can be updated """

        with my_vcr.use_cassette(REPORT_VCR_DIR):
            tasks.update_report()
        
        assert DailyReport.query.count() >= 1
        assert SnowReporter.query.count() >= 1

