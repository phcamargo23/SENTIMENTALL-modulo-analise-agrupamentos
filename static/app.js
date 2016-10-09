(function () {

    angular.module('tcc', ['angular-loading-bar'])
        .controller('MainController', function ($scope, $http) {

            $scope.k = 2
            consultarEntradas();

            function consultarEntradas() {
                $http.get('/entradas').success(function (resultado) {
                    // console.log(resultado);
                    $scope.entradas = resultado;
                    // resultado.forEach(function (value, key) {
                    //     if(value.slice(-7) == 'pending')
                    //         $scope.pending = resultado[key];
                    // })
                });
            }

            $scope.analisar = function () {
                $http.get('/iniciar-analise?k=' + $scope.k).success(function (resultado) {
                    alert(resultado);
                    // console.log(resultado);
                    // var items = [];
                    // Object.keys(dados).forEach(function(key) {
                    //   items.push({key: key, value: dados[key]});
                    // });
                });
            }

            $scope.consultarAnalises = function () {
                $http.get('/consultar-analises').success(function (resultado) {
                    // console.log(resultado);
                    // resultado.forEach(function (value, key) {
                    //     if(value.slice(-7) == 'pending')
                    //         $scope.pending = resultado[key];
                    // })
                    $scope.pending = resultado;
                });
            }

            $scope.consultarProgresso = function (directory) {
                $http.get('/consultar-progresso?directory='+directory).success(function (resultado) {
                    console.log(resultado);
                    // resultado.forEach(function (value, key) {
                    //     if(value.slice(-7) == 'pending')
                    //         $scope.pending = resultado[key];
                    // })
                });
            }

            $scope.consultarResultado = function (directory) {
                $http.get('/consultar-resultado?directory='+directory).success(function (resultado) {
                    // console.log(resultado);
                    $scope.estados = resultado;
                    // resultado.forEach(function (value, key) {
                    //     if(value.slice(-7) == 'pending')
                    //         $scope.pending = resultado[key];
                    // })
                });
            }

            $scope.mostrarResultado = function () {
                if ($scope.objeto == null && $scope.cidade == null && $scope.estado != null) {
                    // console.log('estado: ' + $scope.estado);
                    gerarTreeMapKmeans($scope.estado.kmeans);
                    gerarTreeMapLDA($scope.estado.lda);
                    gerarTreeMapDBSCAN($scope.estado.dbscan);

                } else if ($scope.objeto == null && $scope.cidade != null) {
                    // console.log('cidade: ' + $scope.cidade);
                    gerarTreeMapKmeans($scope.cidade.kmeans);
                    gerarTreeMapLDA($scope.cidade.lda);
                    gerarTreeMapDBSCAN($scope.cidade.dbscan);

                } else if ($scope.objeto != null) {
                    // console.log('objeto: ' + $scope.objeto);
                    gerarTreeMapKmeans($scope.objeto.kmeans);
                    gerarTreeMapLDA($scope.objeto.lda);
                    gerarTreeMapDBSCAN($scope.objeto.dbscan);

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

            function gerarTreeMapDBSCAN(dados) {
                if (dados == null) {
                    alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
                }
                google.charts.load('current', {'packages': ['treemap']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                    var data = new google.visualization.arrayToDataTable(dados);

                    tree = new google.visualization.TreeMap(document.getElementById('chart-dbscan'));

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