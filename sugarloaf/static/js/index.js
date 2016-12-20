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
sugarloaf.parseDate = d3.time.format('%Y-%m-%dT%H:%M:%S');

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
        date['datetime'] = sugarloaf.parseDate.parse(key);
        dates_list.push(date);
    });

    dates_list.sort(function(a, b) {
        if (a.datetime < b.datetime) {
            return -1;
        } else {
            return 1;
        }
    });

    return dates_list;
};

// takes the output of summaryToDates and returns a list of lists ordered by
// Object.keys(sugarloaf.difficulty_order)
function datesToDataset(dates) {
    var output = [];

    Object.keys(sugarloaf.difficulty_order).forEach(function(difficulty) {
        var diff_array = [];

        dates.forEach(function(date) {
            var date_diff_obj = {'x': date.datetime}
            if (undefined === date[difficulty]) {
                date_diff_obj['y'] = 0;
            } else {
                date_diff_obj['y'] = date[difficulty];
            }
            diff_array.push(date_diff_obj)
        })

        output.push(diff_array);
    })
    return output;
}

function countDate(date) {
    var count = 0;
    for (var key in date) {
        if (date.hasOwnProperty(key) && key !== 'datetime') {
            count += date[key];
        }
    }
    return count;
}

function buildSummaryChart(summary) {
    sugarloaf.dates = summaryToDates(summary),
        width = 800 - MARGINS.left - MARGINS.right,
        height = 200 - MARGINS.top - MARGINS.bottom;
    sugarloaf.dataset = datesToDataset(sugarloaf.dates);
    
    sugarloaf.summary_x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1)
        .domain(sugarloaf.dates.map(function(d) {
            return d.datetime;
        }))
    
    sugarloaf.summary_y = d3.scale.linear()
        .rangeRound([height, 0])
        .domain([0, d3.max(sugarloaf.dates, function(d) { return countDate(d)})]);
    
    sugarloaf.summary_stack = d3.layout.stack();
    
    sugarloaf.summary_stack_layers = sugarloaf.summary_stack(sugarloaf.dataset);
    
    sugarloaf.summary_area = d3.svg.area()
        .interpolate('cardinal')
        .x(function(d) { return sugarloaf.summary_x(d.x)})
        .y0(function(d) { return sugarloaf.summary_y(d.y0)})
        .y1(function(d) { return sugarloaf.summary_y(d.y0 + d.y)});
    
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
        .data(sugarloaf.summary_stack_layers)
      .enter().append('path')
          .attr('class', 'layer')
          .attr('d', function(d) { return sugarloaf.summary_area(d);});
}

d3.json(filename_status, function(data) {
    sugarloaf.data = data;

    buildCharts();
});

d3.json(filename_summary, function(data) {
    sugarloaf.summary = data;

    buildSummaryChart(sugarloaf.summary);
});