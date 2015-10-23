(function(){
    var rulesTraits = angular.module('rules.traits', []);

    rulesTraits.controller("TraitsController", ['$scope', function($scope) {

        $scope.$on('switchContent', function (event, args) {
            if (args.targetContent != 'traits'){
                console.log('traits caught switchContent, but ignored (target is '+args.targetContent + ')');
            }
        });

    }]);

    rulesTraits.directive('ruleTraits', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){


        };

        return {
            restrict: 'E',
            controller: 'TraitsController',
            controllerAs: 'traits',
            link: linkFunction
        }
    }]);

})();