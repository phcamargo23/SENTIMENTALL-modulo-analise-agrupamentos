(function () {

    angular.module('tcc', [])
        .controller('MainController', function ($scope, $http, $filter, $interval, $timeout) {

            $scope.analisar = function () {
                $http.get('/analisar?k=' + $scope.k).success(function (resultado) {
                    $scope.estados = resultado;
                    // var items = [];
                    // Object.keys(dados).forEach(function(key) {
                    //   items.push({key: key, value: dados[key]});
                    // });
                });
            }

            $scope.mostrarResultado = function () {
                if ($scope.objeto == null && $scope.cidade == null && $scope.estado != null) {
                    console.log('estado: ' + $scope.estado);
                    gerarVisualizacaoTreeMap($scope.estado.resultado);

                } else if ($scope.objeto == null && $scope.cidade != null) {
                    console.log('cidade: ' + $scope.cidade);
                    gerarVisualizacaoTreeMap($scope.cidade.resultado);

                } else if ($scope.objeto != null) {
                    console.log('objeto: ' + $scope.objeto);
                    gerarVisualizacaoTreeMap($scope.objeto.resultado);

                } else alert('Selecione uma visualização');

            }

            function gerarVisualizacaoTreeMap(dados) {
                if (dados == null) {
                    alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
                }
                google.charts.load('current', {'packages': ['treemap']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                    var data = new google.visualization.arrayToDataTable(dados);

                    tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

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
                            '<span style="font-family:Courier"><b> Cluster ' + data.getValue(row, 0) +'</b> ' +'</span><br>' +
                            data.getColumnLabel(2) + ': ' + size + '<br>' +
                            '</div>';
                    }

                }
            }

        });
})();