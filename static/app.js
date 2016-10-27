'use strict';   // See note about 'use strict'; below

var myApp = angular.module('tcc', [
    'ngRoute', 'angular-loading-bar',
]);

myApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: '/static/views/index.html',
            controller: 'MainController'
        }).when('/entrada', {
            templateUrl: '../static/views/input.html',
            controller: 'InputController'
        }).when('/configuracao', {
            templateUrl: '../static/views/config.html',
            controller: 'ConfigController'
        }).when('/saida', {
            templateUrl: '../static/views/output.html',
            controller: 'OutputController'
        }).otherwise({
            redirectTo: '/'
        });
    }]);


myApp.controller('MainController', function ($scope, $http) {

    consultarResumo();

    function consultarResumo(){
        $http({
            url: '/resumo',
            method: "GET"
        }).success(function (resultado) {
            // alert(resultado);
            // console.log(resultado);
            $scope.resumo = resultado;
        });
    }

    $scope.consultarProgresso = function (directory) {
        $http.get('/consultar-progresso?directory=' + directory).success(function (resultado) {
            console.log(resultado);
            // resultado.forEach(function (value, key) {
            //     if(value.slice(-7) == 'pending')
            //         $scope.pending = resultado[key];
            // })
        });
    }

});

myApp.controller('InputController', function ($scope, $http) {


});

myApp.controller('ConfigController', function ($scope, $http) {
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
        console.log($scope.params.dataset);
        $http({
            url: '/iniciar-analise',
            method: "GET",
            params: {'entrada': $scope.params.dataset, 'k': $scope.params.k, 'n': $scope.params.n, 'eps': $scope.params.eps, 'minPts': $scope.params.minPts}
        }).success(function (resultado) {
            alert(resultado);
        });
    }

});

myApp.controller('OutputController', function ($scope, $http) {

    consultarAnalises();

    function consultarAnalises() {
        $http.get('/consultar-analises').success(function (resultado) {
            // console.log(resultado);
            // resultado.forEach(function (value, key) {
            //     if(value.slice(-7) == 'pending')
            //         $scope.pending = resultado[key];
            // })
            $scope.saidas = resultado;
        });
    }

    $scope.consultarResultado = function (directory) {
        $http.get('/consultar-resultado?directory=' + directory).success(function (resultado) {
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

            var tree = new google.visualization.TreeMap(document.getElementById('chart-kmeans'));

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
                    '<span style="font-family:Courier"><b> Cluster ' + data.getValue(row, 0) + '</b> ' + '</span><br>' +
                    data.getColumnLabel(2) + ': ' + size + '<br>' +
                    '</div>';
            }

        }
    }

    function gerarTreeMapLDA(dados) {
        // if (dados == null) {
        //     alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
        // }
        google.charts.load('current', {'packages': ['treemap']});
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
            var data = new google.visualization.arrayToDataTable(dados);

            var tree = new google.visualization.TreeMap(document.getElementById('chart-lda'));

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
                    '<span style="font-family:Courier"><b> Cluster ' + data.getValue(row, 0) + '</b> ' + '</span><br>' +
                    data.getColumnLabel(2) + ': ' + size + '<br>' +
                    '</div>';
            }

        }
    }

    function gerarTreeMapDBSCAN(dados) {
        // if (dados == null) {
        //     alert('O número de registros da seleção em questão deve ser menor que o número de grupos desejados');
        // }
        google.charts.load('current', {'packages': ['treemap']});
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
            var data = new google.visualization.arrayToDataTable(dados);

            var tree = new google.visualization.TreeMap(document.getElementById('chart-dbscan'));

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
                    '<span style="font-family:Courier"><b> Cluster ' + data.getValue(row, 0) + '</b> ' + '</span><br>' +
                    data.getColumnLabel(2) + ': ' + size + '<br>' +
                    '</div>';
            }

        }
    }
});