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

        //watch the raw data, and when it is available, convert it
        $scope.functions.traits.organize = function(data){
            $scope.data.traits.organized = $scope.functions.ctrl.organizeByCategory(data, 'type');
        };

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