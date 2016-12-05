var filename_status = '/api/current',
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

d3.json(filename_status, function(data) {
    sugarloaf.data = data;

    buildCharts();
});