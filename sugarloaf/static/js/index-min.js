function buildCharts(){sugarloaf.ndx=crossfilter(sugarloaf.data.trails),sugarloaf.openDim=sugarloaf.ndx.dimension(function(r){return r.open?"Open":"Closed"}),sugarloaf.openGroup=sugarloaf.openDim.group().reduceCount(function(r){return r.open}),sugarloaf.openChart=dc.rowChart("#chart-row-open"),sugarloaf.openChart.width(WIDTH).height(HEIGHT/2).margins(MARGINS).dimension(sugarloaf.openDim).group(sugarloaf.openGroup).elasticX(!0),sugarloaf.groomedDim=sugarloaf.ndx.dimension(function(r){return r.groomed?"Groomed":"Ungroomed"}),sugarloaf.groomedGroup=sugarloaf.groomedDim.group().reduceCount(function(r){return r.groomed}),sugarloaf.groomedChart=dc.rowChart("#chart-row-groomed"),sugarloaf.groomedChart.width(WIDTH).height(HEIGHT/2).margins(MARGINS).dimension(sugarloaf.groomedDim).group(sugarloaf.groomedGroup).elasticX(!0),sugarloaf.snowmakingDim=sugarloaf.ndx.dimension(function(r){return r.snowmaking?"Snowmaking in progress":"Not snowmaking"}),sugarloaf.snowmakingGroup=sugarloaf.snowmakingDim.group().reduceCount(function(r){return r.snowmaking}),sugarloaf.snowmakingChart=dc.rowChart("#chart-row-snowmaking"),sugarloaf.snowmakingChart.width(WIDTH).height(HEIGHT/2).margins(MARGINS).dimension(sugarloaf.snowmakingDim).group(sugarloaf.snowmakingGroup).elasticX(!0),sugarloaf.difficultyDim=sugarloaf.ndx.dimension(function(r){return r.difficulty}),sugarloaf.difficultyGroup=sugarloaf.difficultyDim.group().reduceCount(function(r){return r.difficulty}),sugarloaf.difficultyChart=dc.rowChart("#chart-row-difficulty"),sugarloaf.difficultyChart.width(WIDTH).height(HEIGHT).margins(MARGINS).dimension(sugarloaf.difficultyDim).group(sugarloaf.difficultyGroup).ordering(function(r){return sugarloaf.difficulty_order[r.key]}).elasticX(!0),sugarloaf.areaDim=sugarloaf.ndx.dimension(function(r){return r.area}),sugarloaf.areaGroup=sugarloaf.areaDim.group().reduceCount(function(r){return r.area}),sugarloaf.areaChart=dc.rowChart("#chart-row-area"),sugarloaf.areaChart.width(WIDTH).height(2*HEIGHT).margins(MARGINS).dimension(sugarloaf.areaDim).group(sugarloaf.areaGroup).elasticX(!0),dc.renderAll()}var filename_status="/api/current",WIDTH=300,HEIGHT=200,MARGINS={top:10,left:20,right:20,bottom:20},sugarloaf={};sugarloaf.difficulty_order={beginner:1,intermediate:2,black:3,"double-black":4,"terrain-park":5},d3.json(filename_status,function(r){sugarloaf.data=r,buildCharts()});