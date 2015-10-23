(function(){
    var rulesSections = angular.module('rules.sections', []);

    rulesSections.controller("SectionsController", ['$http', '$scope', function($http, $scope) {
        $scope.tree = [];

        //section request data
        $scope.sectionsRequestSent = false;
        $scope.sectionsDataReceived = false;

        $scope.$on('switchContent', function(event, args) {
            if (args.targetContent != 'sections'){
                console.log('sections caught switchContent, but ignored (target is '+args.targetContent + ')');
            }
            else {
                $scope.getTree();
            }
        });

        //function to dynamically add child based on list of depths
        function addChild(tree, depth, data){
            //get tree
            var section = tree;

            //for each depth except the last one...
            for (var i = 0; i < depth.length - 1; i++){

                //get the parent
                if (i == 0) {
                    section = section[depth[i]];
                }
                //and then get the each child in succession
                else {
                    section = section.children[depth[i]];
                }
            }
            //then set the child equal to the section data
                //since we didn't use the last item in the depth list,
                //we can use that as the child num. this keeps the depth string
                //perfectly valid for all current and future children
            section['children'][depth[depth.length-1]] = sectionData(data);

            return tree;
        }

        //single function to organize data & reduce clutter
        function sectionData(data){
            return {
                title: data.title,
                slug: slugify(data.title),
                content: data.content,
                tier: data.tier,
                type: data.type,
                topParent: slugify(data.topParent),
                children: []
            }
        }

        function organizeSections(json){
            //set vars out of loop to reduce process time
            var tier = 0;
            var depth = 0;
            var tree = [];
            var topParent = "";

            //loop through every item
            for (var i = 0; i < json.length; i++){
                //set depth and tier vars
                depth = json[i].fields.depth_string.split('.');
                tier = depth.length;
                //set tier in data
                json[i].fields.tier = tier;
                //set topParent if tier 1
                if (tier == 1) topParent = json[i].fields.title;
                //set all parents regardless of tier (tier 1 will be their own parent)
                json[i].fields.topParent = topParent;

                //if parent, add to top
                if (tier == 1){
                    tree[depth[0]] = sectionData(json[i].fields);
                }
                //otherwise, use depth list to add a child and send json data
                else {
                    addChild(tree, depth, json[i].fields);
                }
            }

            //return the final tree value
            return tree;
        }

        //variable function to get tree
        $scope.getTree = function(callback){
            //if called without callback, make a fake callback function
            if (callback == null){
                callback = function(){};
            }
            //check if data has been requested
            if(!$scope.sectionsRequestSent){
                //store that we have requested data
                $scope.sectionsRequestSent = true;
                //toast
                Materialize.toast('Loading rules...', 2000);
                //async get section data
                $scope.getSectionsPromise = $http.get('json/section').then(function(response) {
                    //get json
                    var json = response.data;
                    //organize the data
                    $scope.tree = organizeSections(json);
                    //tell the app that we are done organizing the data
                    $scope.sectionsDataOrganized = true;
                    //after data set, callback
                    callback();
                });
            }
            else {
                // if we get here, that means the request has already been sent
                // check if DataReceived is true, and run callback if so
                if ($scope.sectionsDataOrganized == true){
                    setTimeout(function(){
                        callback();
                    }, 0);
                }
                else {
                    // otherwise, watch the DataReceived var, and when it changes to true, do the callback
                    $scope.$watch(function($scope){ return $scope.sectionsDataOrganized},
                        function(){
                            if ($scope.sectionsDataOrganized == true){
                                callback();
                            }
                    });
                }
            }
        };
    }]);

    rulesSections.directive('ruleSections', ['$compile', function($compile){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
            //when this exists, switch content to this
            $scope.$emit('ctrlSwitchContent', {targetContent: 'sections'});
            beginContentLoad($scope.fadeTime);

            var afterSectionsCompile = function() {
                    //make it set itself to the end
                    setTimeout(function () {
                        //if it doesn't detect that the rules are done loading, it ends itself and calls itself again with
                        //a delay of $scope.retryTime
                        if ($('.rule-section').length < 100 || $('.section-bookmark-link').length < 100) {
                            afterSectionsCompile();
                            return
                        }
                        //inject the content, and do fades
                        setRulesContent($('.rules-sections'), $('.rules-sections-left'), $scope.fadeTime);
                        //then run the js to hook to current content
                        sectionsLoaded();
                        //set active section
                        $scope.loaded.sections = true;
                        $scope.active = 'sections';
                    }, $scope.retryTime);
                };

            //run the after function
            afterSectionsCompile();

        };

        return {
            restrict: 'E',
            templateUrl: '/static/html/rules/sections/rule-sections.html',
            controller: 'SectionsController',
            controllerAs: 'sections',
            link: linkFunction
        }
    }]);

})();
