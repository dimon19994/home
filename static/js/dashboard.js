for (var block_id in min) {
    $("<h1>"+block_id+"</h1>\n" +
        "<div id='"+block_id+"' class='"+block_id+"'>\n" +
        "</div>").insertBefore($("p"));
}

for (var block_id in graphs) {
    layout = {
        yaxis: {
            title: {text: 'CHISLA'},
            tickvals: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            ticktext: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        },
        xaxis: {

            range: [-1 * min[block_id] - 2, min[block_id] + 2],
            tickvals: [-1 * min[block_id], Math.floor((-1 * min[block_id]) / 4 * 3), Math.floor((-1 * min[block_id]) / 4 * 2), Math.floor((-1 * min[block_id]) / 4), 0, Math.ceil((min[block_id]) / 4), Math.ceil((min[block_id]) / 4 * 2), Math.ceil((min[block_id]) / 4 * 3), min[block_id]],
            ticktext: [min[block_id], Math.ceil((min[block_id]) / 4 * 3), Math.ceil((min[block_id]) / 4 * 2), Math.ceil((min[block_id]) / 4), 0, Math.ceil((min[block_id]) / 4), Math.ceil((min[block_id]) / 4 * 2), Math.ceil((min[block_id]) / 4 * 3), min[block_id]],
            title: {text: 'CHASTOTA'}
        },
        barmode: 'overlay',
        bargap: 0.1
    }

    Plotly.plot(block_id, {data: [graphs[block_id][0], graphs[block_id][1]], layout: layout}, {});
}
