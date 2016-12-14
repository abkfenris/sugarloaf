var filename_status = '/api/current',
    filename_summary = '/api/summary',
    WIDTH = 300,
    HEIGHT = 200,
    MARGINS = {top: 10, left: 20, right: 20, bottom: 20},
    sugarloaf = {};

sugarloaf.difficulty_order = {
    'beginner': 1,
    'intermediate': 2,
    'black': 3,
    'double-black': 4,
    'terrain-park': 5
}

function buildCharts() {
    sugarloaf.ndx = crossfilter(sugarloaf.data.trails);

    sugarloaf.openDim = sugarloaf.ndx.dimension(function(d) {
        if (d.open) {
            return 'Open';
        } else {
            return 'Closed';
        };
    });
    sugarloaf.openGroup = sugarloaf.openDim.group().reduceCount(function(d) {
        return d.open;
    });
    sugarloaf.openChart = dc.rowChart('#chart-row-open');
    sugarloaf.openChart
        .width(WIDTH)
        .height(HEIGHT/2)
        .margins(MARGINS)
        .dimension(sugarloaf.openDim)
        .group(sugarloaf.openGroup)
        .elasticX(true);


    sugarloaf.groomedDim = sugarloaf.ndx.dimension(function(d) {
        if (d.groomed) {
            return 'Groomed';
        } else {
            return 'Ungroomed';
        }
    });
    sugarloaf.groomedGroup = sugarloaf.groomedDim.group().reduceCount(function(d) {
        return d.groomed;
    })
    sugarloaf.groomedChart = dc.rowChart('#chart-row-groomed');
    sugarloaf.groomedChart
        .width(WIDTH)
        .height(HEIGHT/2)
        .margins(MARGINS)
        .dimension(sugarloaf.groomedDim)
        .group(sugarloaf.groomedGroup)
        .elasticX(true);
    

    sugarloaf.snowmakingDim = sugarloaf.ndx.dimension(function(d) {
        if (d.snowmaking) {
            return 'Snowmaking in progress';
        } else {
            return 'Not snowmaking';
        }
    });
    sugarloaf.snowmakingGroup = sugarloaf.snowmakingDim.group().reduceCount(function(d) {
        return d.snowmaking;
    });
    sugarloaf.snowmakingChart = dc.rowChart('#chart-row-snowmaking');
    sugarloaf.snowmakingChart
        .width(WIDTH)
        .height(HEIGHT/2)
        .margins(MARGINS)
        .dimension(sugarloaf.snowmakingDim)
        .group(sugarloaf.snowmakingGroup)
        .elasticX(true);

    sugarloaf.difficultyDim = sugarloaf.ndx.dimension(function(d) {
        return d.difficulty;
    });
    sugarloaf.difficultyGroup = sugarloaf.difficultyDim.group().reduceCount(function(d) {
        return d.difficulty;
    });
    sugarloaf.difficultyChart = dc.rowChart('#chart-row-difficulty');
    sugarloaf.difficultyChart
        .width(WIDTH)
        .height(HEIGHT)
        .margins(MARGINS)
        .dimension(sugarloaf.difficultyDim)
        .group(sugarloaf.difficultyGroup)
        .ordering(function(d) {
            return sugarloaf.difficulty_order[d.key];
        })
        .elasticX(true);
    
    
    sugarloaf.areaDim = sugarloaf.ndx.dimension(function(d) {
        return d.area;
    });
    sugarloaf.areaGroup = sugarloaf.areaDim.group().reduceCount(function(d) {
        return d.area;
    });
    sugarloaf.areaChart = dc.rowChart('#chart-row-area');
    sugarloaf.areaChart
        .width(WIDTH)
        .height(HEIGHT * 2)
        .margins(MARGINS)
        .dimension(sugarloaf.areaDim)
        .group(sugarloaf.areaGroup)
        .elasticX(true);

    dc.renderAll();
}

function summaryToDates(summary) {
    var dates = {};

    summary.conditions.forEach(function(c) {
        // set our initial date if unknown
        if (undefined === dates[c.datetime]) {
            dates[c.datetime] = {};
        }

        // make our difficulties
        if (c.open && undefined === dates[c.datetime][c.difficulty]) {
            dates[c.datetime][c.difficulty] = c.trail_count;
        } else if (c.open) {
            dates[c.datetime][c.difficulty] += c.trail_count;
        } else if (undefined === dates[c.datetime]['closed']) {
            dates[c.datetime]['closed'] = c.trail_count;
        } else {
            dates[c.datetime]['closed'] += c.trail_count;
        };
    });

    var dates_list = [];

    Object.keys(dates).forEach(function(key) {
        var date = dates[key];
        date['datetime'] = key;
        dates_list.push(date);
    });

    return dates_list;
};


function buildSummaryChart(summary) {
    var dates = summaryToDates(summary),
        width = 800 - MARGINS.left - MARGINS.right,
        height = 200 - MARGINS.top - MARGINS.bottom;
    
    sugarloaf.summary_x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1)
        .domain(dates.map(function(d) {
            return d.datetime;
        }))
    
    sugarloaf.summary_y = d3.scale.linear()
        .rangeRound([height, 0]);
    
    sugarloaf.summary_stack = d3.layout.stack()
        .offset('zero')
        .values(function(d) {return d.values;})
        .x(function(d) {return x(d.datetime)})
        .y(function(d) {return d.value});
    
    sugarloaf.summary_color = d3.scale.ordinal()
        //     green,      blue,     black, double-black, terrain-park closed
        .range(['#05FF00', '#0040FF', '#6D6D6D', '#000', '#F6AE3B', '#FFF'])
        .domain(['green', 'blue', 'black', 'double-black', 'terrain-park', 'closed']);

    var svg = d3.select('#chart-summary').append('svg')
        .attr('width', width + MARGINS.left + MARGINS.right)
        .attr('height', height + MARGINS.top + MARGINS.bottom)
      .append('g')
        .attr('transform', 'translate(' + MARGINS.left + ',' + MARGINS.top +')');
    
    var selection = svg.selectAll('.series')
        .data(dates)
        .enter().append('g')
          .attr('class', 'series');
}

d3.json(filename_status, function(data) {
    sugarloaf.data = data;

    buildCharts();
});

d3.json(filename_summary, function(data) {
    sugarloaf.summary = data;

    buildSummaryChart(sugarloaf.summary);
});