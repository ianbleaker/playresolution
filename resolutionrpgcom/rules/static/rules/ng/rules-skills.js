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

        $scope.$on('switchContent', function (event, args) {
            if (args.targetContent != 'skills'){
                console.log('skills caught switchContent, but ignored (target is '+args.targetContent + ')');
            }
        });

        function organizeSkills(data){
            var output = {};
            for (var i = 0; i < data.length; i++){
                if (!output[data[i].skill_class]){
                    output[data[i].skill_class] = {};
                    output[data[i].skill_class].name = data[i].skill_class;
                    output[data[i].skill_class].skills = [];
                }
                output[data[i].skill_class].skills.push(data[i]);
                output[data[i].skill_class].skills.sort(function(a,b) {return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);} );
            }

            return output;
        }

        //watch the raw data, and when it is available, convert it
        $scope.$watch(function($scope){return $scope.data.skills.raw},
            function(newValue, oldValue){
                if ($scope.status.skills.dataRetrieved) {
                    $scope.data.skills.organized = organizeSkills($scope.data.skills.raw);
                }
            }
        );

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