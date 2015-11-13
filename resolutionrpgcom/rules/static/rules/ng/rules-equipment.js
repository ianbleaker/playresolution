(function(){
    var rulesEquipment = angular.module('rules.equipment', []);

    rulesEquipment.controller("EquipmentController", ['$scope', function($scope) {

        //set up content controller stuff
        $scope.data.equipment = {};
        $scope.status.equipment = {
            dataRequestSent: false,
            dataRetrieved: false
        };
        $scope.promises.equipment = {};
        $scope.functions.equipment = {};

        //watch the raw data, and when it is available, convert it
        $scope.functions.equipment.organize = function(data){
            $scope.data.equipment.organized = data;
        };

    }]);

    rulesEquipment.directive('ruleEquipment', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
        };

        return {
            restrict: 'E',
            controller: 'EquipmentController',
            controllerAs: 'equipment',
            link: linkFunction
        }
    }]);

})();