(function () {

    angular.module('tcc', [])
        .controller('MainController', function ($scope, $http, $filter, $interval, $timeout) {

        // $scope.fit = function() {
            $http.get('/kmeans').success(function(data){
                console.log(data);
            });
        // };
        });
})();