import vcr

REPORT_VCR_DIR = 'tests/fixtures/vcr/reports.yaml'

my_vcr = vcr.VCR(
    record_mode='new_episodes'
)