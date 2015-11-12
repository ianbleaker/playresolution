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

        $scope.functions.skills.organizeInList = function(data) {
            var output = [];

            for (var i = 0; i < data.length; i++){
                //stringify specializations
                var specializations = [];
                for (var j = 0; j < data[i].specializations.length; j++) specializations.push(data[i].specializations[j].name);
                if(specializations[0] == undefined) specializations = data[i].specialization_text;
                else specializations = specializations.sort().join(', ');

                //stringify types
                var types = [];
                for (var k = 0; k < data[i].types.length; k++) types.push(data[i].types[k].name);
                if(types[0] == undefined) types = "Not a typed skill.";
                else types = types.sort().join(', ');

                var skill = {
                    name: data[i].name,
                    base_aptitude: data[i].base_aptitude.name,
                    skill_class: data[i].skill_class,
                    what: data[i].what,
                    when: data[i].when,
                    specialization_text: data[i].specialization_text,
                    types: types,
                    specializations: specializations
                };

                output.push(skill);
            }

            return output;
        };

        $scope.functions.skills.organize = function(data){
            $scope.data.skills.list = $scope.functions.skills.organizeInList(data);
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