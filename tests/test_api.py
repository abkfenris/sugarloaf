#! ../env/bin/python
# -*- coding: utf-8 -*-

import json

import pytest

from sugarloaf import tasks

from .shared import my_vcr, REPORT_VCR_DIR

@pytest.mark.usefixtures("testapp")
class TestApi:
    def test_current_api(self, testapp):
        """ Test that the current api endpoint will return trail updates """

        with my_vcr.use_cassette(REPORT_VCR_DIR):
            tasks.update_trails_lifts()
            tasks.update_report()
        
        rv = testapp.get('/api/current')
        assert rv.status_code == 200
        assert 'SuperQuad' in str(rv.data)
        assert 'Lower Narrow Gauge' in str(rv.data)

        data = json.loads(rv.data.decode())

        assert 'Sun, 11 Dec 2016 12:00:00 GMT' == data['datetime']

        trail_names = [trail['name'] for trail in data['trails']]
        assert 'Branding Ax Glade' in trail_names
        assert 'Upper Rookie River Glade' in trail_names
        assert 'Cant Dog One' in trail_names

        lift_names = [lift['name'] for lift in data['lifts']]
        assert 'Skyline' in lift_names
        assert 'King Pine' in lift_names
    
    def test_summary_api(self, testapp):
        """ Test that the summary api will return conditions for the whole season """

        with my_vcr.use_cassette(REPORT_VCR_DIR):
            tasks.update_trails_lifts()
            tasks.update_report()
        
        rv = testapp.get('/api/summary')
        assert rv.status_code == 200

        data = json.loads(rv.data.decode())

        assert 'conditions' in data
        assert isinstance(data['conditions'], list)

        assert 'datetime' in data['conditions'][0]
        assert 'open' in data['conditions'][0]
        assert isinstance(data['conditions'][0]['trail_count'], int)
