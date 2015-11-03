(function(){
    var rulesTables = angular.module('rules.tables', []);

    rulesTables.controller("TablesController", ['$scope', function($scope) {

        $scope.functions.tables = {};

    }]);

    rulesTables.directive('ruleTables', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
            $scope.functions.tables.load = function(){
                Materialize.toast('load tables', 2000);
            }

        };

        return {
            restrict: 'E',
            controller: 'TablesController',
            controllerAs: 'tables',
            link: linkFunction
        }
    }]);

})();