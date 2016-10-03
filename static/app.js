(function () {

    angular.module('tcc', [])
        .controller('MainController', function ($scope, $http, $filter, $interval, $timeout) {
            // var dados;
            // $scope.estado = 'PE'

            $scope.mostrarResultado = function () {
                if($scope.objeto == null && $scope.cidade == null && $scope.estado != null){
                    console.log('estado: '+$scope.estado);
                    visualizar($scope.estado.resultado);

                }else if($scope.objeto == null && $scope.cidade != null) {
                    console.log('cidade: ' + $scope.cidade);
                    visualizar($scope.cidade.resultado);

                }else if($scope.objeto != null) {
                    console.log('objeto: ' + $scope.objeto);
                    visualizar($scope.objeto.resultado);

                }else alert('Selecione uma visualização');

            }

            // $scope.listarCidades = function (estado) {
            //     // console.log(estado);
            //     // console.log($scope.estados)
            //     // console.log($scope.estados[estado])
            //     // console.log($scope.estados.estado);
            //     $scope.cidades = estado;
            // }

            $http.get('/analisar?k=3').success(function (resultado) {
                // dados = resultado;
                $scope.estados = resultado;
                // $scope.cidades = dados[$scope.estado];
                // console.log($scope.estados);
                // $scope.cidades = dados['cidades']
                // $scope.objetos = dados['objetos']

                // var items = [];
                // Object.keys(dados).forEach(function(key) {
                //   items.push({key: key, value: dados[key]});
                // });
                // console.log(items);

                // visualizar(dados['estados'][$scope.estado])
            });

            function visualizar(dados) {
                if(dados == null){
                    alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
                    // google.charts.clearChart;
                    // return;
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
                            '<span style="font-family:Courier"><b>' + data.getValue(row, 0) +
                            '</b>, ' + data.getValue(row, 1) + ', ' + data.getValue(row, 2) +
                            '</span><br>' +
                            'Datatable row: ' + row + '<br>' +
                            data.getColumnLabel(2) + ' : ' + size + '<br>' +
                            '</div>';
                    }

                }
            }

        });
})();