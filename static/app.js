(function () {

    angular.module('tcc', ['angular-loading-bar'])
        .controller('MainController', function ($scope, $http) {

            $scope.analisar = function () {
                $http.get('/analisar?k=' + $scope.k).success(function (resultado) {
                    $scope.estados = resultado;
                    console.log(resultado);
                    // var items = [];
                    // Object.keys(dados).forEach(function(key) {
                    //   items.push({key: key, value: dados[key]});
                    // });
                });
            }

            $scope.mostrarResultado = function () {
                if ($scope.objeto == null && $scope.cidade == null && $scope.estado != null) {
                    console.log('estado: ' + $scope.estado);
                    gerarTreeMapKmeans($scope.estado.kmeans);
                    gerarTreeMapLDA($scope.estado.lda);

                } else if ($scope.objeto == null && $scope.cidade != null) {
                    console.log('cidade: ' + $scope.cidade);
                    gerarTreeMapKmeans($scope.cidade.kmeans);
                    gerarTreeMapLDA($scope.estado.lda);

                } else if ($scope.objeto != null) {
                    console.log('objeto: ' + $scope.objeto);
                    gerarTreeMapKmeans($scope.objeto.kmeans);
                    gerarTreeMapLDA($scope.estado.lda);

                } else alert('Selecione uma visualização');

            }

            function gerarTreeMapKmeans(dados) {
                if (dados == null) {
                    alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
                }
                google.charts.load('current', {'packages': ['treemap']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                    var data = new google.visualization.arrayToDataTable(dados);

                    tree = new google.visualization.TreeMap(document.getElementById('chart-kmeans'));

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

            function gerarTreeMapLDA(dados) {
                if (dados == null) {
                    alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
                }
                google.charts.load('current', {'packages': ['treemap']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                    var data = new google.visualization.arrayToDataTable(dados);

                    tree = new google.visualization.TreeMap(document.getElementById('chart-lda'));

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