(function(){
    var rulesTables = angular.module('rules.tables', []);

    rulesTables.controller("TablesController", ['$scope', function($scope) {

        $scope.status.tables = {active: 'traits'};
        $scope.functions.tables = {};
        $scope.functions.tables.after = function(){
            console.log('function');
        }

    }]);

    rulesTables.directive('ruleTables', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){

            $scope.functions.tables.load = function(){
                beginContentLoad($scope.fadeTime);

                var afterLoad = function(){
                    setRulesContent({pageContent: $('.traits-table')});
                    $('#traits-table').find('table').dynatable({
                        features: {
                            paginate: false,
                            recordCount: false,
                            pushState: false
                        },
                        dataset: {
                            records: $scope.data.traits.raw
                        },
                        table: {
                            defaultColumnIdStyle: 'underscore'
                        }
                    });
                };

                $scope.functions.ctrl.get('traits', afterLoad);
            }

        };

        return {
            restrict: 'E',
            controller: 'TablesController',
            templateUrl: '/static/html/rules/tables/tables.html',
            controllerAs: 'tables',
            link: linkFunction
        }
    }]);

})();