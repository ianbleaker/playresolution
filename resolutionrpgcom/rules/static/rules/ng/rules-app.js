(function(){
    var app = angular.module('rules', ['rules.sections', 'rules.traits', 'rules.skills', 'rules.tables']);

    app.controller("ContentController", ['$scope', '$http', function($scope, $http){
        //logo text
        $scope.logo = {navbar: {}, left: {}};
        $scope.logo.navbar.before = 'rez';
        $scope.logo.navbar.after = 'rules';
        $scope.logo.left.before = 'rules';
        $scope.logo.left.after = 'sections';

        //scope time constants
        $scope.retryTime = 100;
        $scope.fadeTime = 700;

        //containers to track status, promises, functions, data
        $scope.status = { active: '' };
        $scope.promises = {};
        $scope.functions = {};
        $scope.functions.ctrl = {};
        $scope.data = {};

        //watch the active part
        $scope.$watch(function(){ return $scope.status.active },
            function(newValue, oldValue){
                //if active changes, and new value is real and isn't the same as the old one
                if(newValue != "" && newValue != oldValue){
                    //if there is an unload function for the old content, run that
                    if (oldValue != "" && $scope.functions[oldValue].unload != undefined) {
                        $scope.functions[oldValue].unload();
                    }
                    //load content based on new value
                    $scope.functions[newValue].load();
                }
            }
        );

        $scope.functions.ctrl.get = function(contentName, args){
            //handle no args
            if (!args) args = {};
            //only do anything if the data hasn't been requested yet
            if(!$scope.status[contentName].dataRequestSent){
                //store that we have requested data
                $scope.status[contentName].dataRequestSent = true;
                //toast
                if (args.toast){
                     Materialize.toast(args.toast, 1500);
                }
                $scope.promises[contentName].get = $http.get('json/' + contentName).then(
                    function(response) {
                        //tell the app that we are done retrieving the data
                        $scope.status[contentName].dataRetrieved = true;
                        //save the raw data
                        $scope.data[contentName].raw = response.data;
                    });
            }
        };

        $scope.functions.ctrl.checkLoaded = function(contentName, callback){
            setTimeout(function(){
                    //blank function if none sent
                if (callback == null){
                    callback = function(){};
                }
                //if the stuff isn't loaded yet..
                if(!$scope.status[contentName].loaded){
                    //wait a little bit, then..
                    setTimeout(function(){
                        //if the stuff is organized
                        if($scope.data[contentName].organized != undefined){
                            //tell the app that this content is loaded
                            $scope.status[contentName].loaded = true;
                        }
                        //redo this function no matter what
                        $scope.functions.ctrl.checkLoaded(contentName, callback);
                    }, $scope.retryTime);
                }
                else {
                    setTimeout(function(){
                        callback();
                    }, $scope.retryTime);
                }
            }, $scope.retryTime);
        };

    }]);

    //create a filter to allow binding to raw html
    app.filter('rawHtml', ['$sce', function($sce){
      return function(val) {
        return $sce.trustAsHtml(val);
      };
    }]);

})();
