(function(){
    var rulesTraits = angular.module('rules.traits', []);

    rulesTraits.controller("TraitsController", ['$scope', function($scope) {

        //set up content controller stuff
        $scope.data.traits = {};
        $scope.status.traits = {
            dataRequestSent: false,
            dataRetrieved: false,
            loaded: false
        };
        $scope.promises.traits = {};
        $scope.functions.traits = {};

        function organizeTraits(data){
            var output = {};
            for (var i = 0; i < data.length; i++){
                if (!output[data[i].type]){
                    output[data[i].type] = {};
                    output[data[i].type].name = data[i].type;
                    output[data[i].type].traits = [];
                }
                output[data[i].type].traits.push(data[i]);
                output[data[i].type].traits.sort(function(a,b) {return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);} );
            }

            return output;
        }

        //watch the raw data, and when it is available, convert it
        $scope.$watch(function($scope){return $scope.data.traits.raw},
            function(newValue, oldValue){
                if ($scope.status.traits.dataRetrieved) {
                    $scope.data.traits.organized = organizeTraits(newValue);
                }
            }
        );

    }]);

    rulesTraits.directive('ruleTraits', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
        };

        return {
            restrict: 'E',
            templateUrl: '/static/html/rules/traits/traits.html',
            controller: 'TraitsController',
            controllerAs: 'traits',
            link: linkFunction
        }
    }]);

})();