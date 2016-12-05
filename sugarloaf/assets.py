from flask_assets import Bundle

common_css = Bundle(
    'css/vendor/bootstrap.min.css',
    'css/vendor/helper.css',
    'css/main.css',
    filters='cssmin',
    output='public/css/common.css'
)

dc_css = Bundle(
    'css/vendor/dc.css',
    #'css/vendor/leaflet.css',
    filters='cssmin',
    output='public/css/dc.css'
)

common_js = Bundle(
    'js/vendor/jquery.min.js',
    'js/vendor/bootstrap.min.js',
    Bundle(
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)

dc_js = Bundle(
    'js/vendor/d3.js',
    'js/vendor/crossfilter.js',
    'js/vendor/dc.js',
    output='public/js/d3_dc.js'
)

index_js = Bundle(
    'js/index.js',
    filters='jsmin',
    output='public/js/index.js'
)