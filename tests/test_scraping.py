#! /usr/bin/env python
# -*- coding: utf-8 -*-

from sugarloaf.helpers import scrape_sugarloaf_lifts_trails as lt
from sugarloaf.helpers import scrape_sugarloaf_report as report

from .shared import my_vcr, REPORT_VCR_DIR

class TestScraping:
    
    def test_scrape_trails(self):
        """ Test if scraping sugarloaf's trails work """

        with my_vcr.use_cassette(REPORT_VCR_DIR):
            soup = lt.make_soup()
        
        trails = lt.update_trails(soup)
        trail_names = [trail['name'] for trail in trails]
        assert 'Middle Narrow Gauge' in trail_names
        assert 'Lower Winters Way' in trail_names
        assert 'Snowbrook' in trail_names
    
    def test_scrape_lifts(self):
        """ Test if scraping sugarloaf's lifts work"""

        with my_vcr.use_cassette(REPORT_VCR_DIR):
            soup = lt.make_soup()
        
        lifts = lt.update_lifts(soup)
        lift_names = [lift['name'] for lift in lifts]
        assert 'King Pine' in lift_names
        assert 'Double Runner East' in lift_names
        assert 'Whiffletree SuperQuad' in lift_names
        assert 'Snubber' in lift_names
    
    def test_scrape_datetime(self):
        """ Test if scraping sugarloaf's lift and trail report gives an accurate datetime """
        
        with my_vcr.use_cassette(REPORT_VCR_DIR):
            soup = lt.make_soup()
        
        dt = lt.update_time(soup)
        assert 2016 == dt.year
        assert 12 == dt.month
        assert 11 == dt.day
        assert 12 == dt.hour
        assert 0 == dt.minute
    
    def test_scrape_report(self):
        """ Test if the daily report can be scraped """
        
        with my_vcr.use_cassette(REPORT_VCR_DIR):
            soup = report.make_soup()
        
        daily_report = report.report_text(soup)
        assert 'Good Sunday morning!' in daily_report
        assert 'Sugarloafers' in daily_report
    

    def test_scrape_report_datetime(self):
        """ Test if the daily report datetime can be scraped """

        with my_vcr.use_cassette(REPORT_VCR_DIR):
            soup = report.make_soup()
        
        dt = report.update_time(soup)
        assert 2016 == dt.year
        assert 12 == dt.month
        assert 11 == dt.day
        assert 7 == dt.hour
        assert 5 == dt.minute
    
    def test_scrape_reporter(self):
        """ Test if the daily report reporter can be scraped """
        with my_vcr.use_cassette(REPORT_VCR_DIR):
            soup = report.make_soup()
        
        reporter = report.report_reporter(soup)
        assert 'Sarah Sindo' == reporter