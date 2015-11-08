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
                var afterLoad = function(){
                    setRulesContent({pageContent: '<table id="tables-table" class="table dynamic-table"></table>'});
                    var table = $('#tables-table');
                    $(table).dataTable({
                        sDom: '<"dynamic-table-wrapper"t>',
                        paging: false,
                        stateSave: false,
                        data: $scope.data.traits.raw,
                        columns: [
                            {title: 'Name', data: 'name'},
                            {title: 'Type', data: 'type'},
                            {title: 'Value', data: 'value'},
                            {title: 'Short Description', data: 'short_description'}
                        ]
                    });
                    contentLoaders({begin: false, fadeTime: $scope.fadeTime});
                };

                $scope.functions.ctrl.get('traits', {
                    toast: 'Loading tables..',
                    before: [contentLoaders, {begin: true, fadeTime: $scope.fadeTime}],
                    after: afterLoad
                });
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