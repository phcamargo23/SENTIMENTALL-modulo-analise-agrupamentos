(function () {

    angular.module('tcc', [])
        .controller('MainController', function ($scope, $http, $filter, $interval, $timeout) {

            $http.get('/analisar?k=3').success(function (dados) {
                t = [];
                angular.forEach(dados, function (value, key) { //Percorre clusters
                    t.unshift([key.toString(), 'clusters', 0]);
                    angular.forEach(value, function (v, k) { //Percorre aspecto/centroides
                        v.splice(1, 0, key.toString());
                        v[0] = v[0] + '(' + key.toString() + ')';
                        t.push(v);
                    });

                });

                t.unshift(['clusters', null, 0]);
                t.unshift(['cluster', 'pai', 'centroide']);

                google.charts.load('current', {'packages': ['treemap']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                    var data = google.visualization.arrayToDataTable(t);

                    tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

                    var options = {
                        minColor: '#f00',
                        midColor: '#ddd',
                        maxColor: '#0d0',
                        headerHeight: 15,
                        fontColor: 'black'
                    };

                    var options = {
                        minColor: '#e7711c',
                        midColor: '#fff',
                        maxColor: '#4374e0',
                        showScale: true,
                        generateTooltip: showFullTooltip
                    };

                    tree.draw(data, options);

                    function showFullTooltip(row, size, value) {
                        return '<div style="background:#fd9; padding:10px; border-style:solid">' +
                                '<span style="font-family:Courier"><b>' + data.getValue(row, 0) +
                                '</b>, ' + data.getValue(row, 1) + ', ' + data.getValue(row, 2) +
                                '</span><br>' +
                                'Datatable row: ' + row + '<br>' +
                                data.getColumnLabel(2) +' : ' + size + '<br>'+
                            '</div>';
                    }

                }


            });
            // };
        });
})();