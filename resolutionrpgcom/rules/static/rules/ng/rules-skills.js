(function(){
    var rulesSkills = angular.module('rules.skills', []);

    rulesSkills.controller("SkillsController", ['$scope', '$http', function($scope, $http) {

        //set up content controller stuff
        $scope.data.skills = {};
        $scope.status.skills = {
            dataRequestSent: false,
            dataReceived: false,
            loaded: false
        };
        $scope.promises.skills = {};
        $scope.functions.skills = {};

        $scope.functions.skills.organize = function(data){
            $scope.data.skills.organized = $scope.functions.ctrl.organizeByCategory(data, 'skill_class');
        };

    }]);

    rulesSkills.directive('ruleSkills', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
        };

        return {
            restrict: 'E',
            templateUrl: '/static/html/rules/skills/skills.html',
            controller: 'SkillsController',
            controllerAs: 'skills',
            link: linkFunction
        }
    }]);

})();