(function(){
    var app = angular.module('rules', ['rules.sections']);

    //create a filter to allow binding to raw html
    app.filter('rawHtml', ['$sce', function($sce){
      return function(val) {
        return $sce.trustAsHtml(val);
      };
    }]);

})();
