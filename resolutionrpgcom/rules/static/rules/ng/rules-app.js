(function(){
    var app = angular.module('rules', ['rules.sections', 'rules.traits']);

    app.controller("ContentController", ['$scope', '$rootScope', function($scope, $rootScope){
        //logo text
        $scope.navbarLogoBefore = 'rez';
        $scope.navbarLogoAfter = 'rules';
        $scope.leftMenuLogoBefore = 'rules';
        $scope.leftMenuLogoAfter = 'sections';

        //scope time constants
        $scope.retryTime = 50;
        $scope.fadeTime = 700;

        //track which sections have been loaded
        $scope.loaded = {
            sections: {
                dataRequestSent: false,
                dataReceived: false,
                data
            },
            traits: false
        };

        //track active content
        $scope.active = 'sections';

        //when switch content is called, do something
        $scope.$on('ctrlSwitchContent', function(event, args){
            setTimeout(function() {
                $scope.$broadcast('switchContent', args);
            }, 0);
        });

    }]);

    //create a filter to allow binding to raw html
    app.filter('rawHtml', ['$sce', function($sce){
      return function(val) {
        return $sce.trustAsHtml(val);
      };
    }]);

})();
