(function(){
    var rulesSections = angular.module('rules.sections', []);

    rulesSections.controller("SectionsController", ['$http', '$scope', '$log', '$timeout', function($http, $scope, $log, $timeout) {
        //create ref to this, create tree
        var ctrl = this;
        $scope.tree = [];

        //scope request data
        $scope.sectionsRequestSent = false;
        $scope.sectionsDataReceived = false;

        //scope callback times
        $scope.retryTime = 50;
        $scope.fadeTime = 700;

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
                    $scope.sectionsDataReceived = true;
                    //after data set, callback
                    callback();
                });
            }
            else {
                // if we get here, that means the request has already been sent
                // check if DataReceived is true, and run callback if so
                if ($scope.sectionsDataReceived == true){
                    callback();
                }
                else {
                    // otherwise, watch the DataReceived var, and when it changes to true, do the callback
                    $scope.$watch(function($scope){ return $scope.sectionsDataReceived},
                        function(){
                            if ($scope.sectionsDataReceived == true){
                                callback();
                            }
                    });
                }
            }
        };
    }]);

    rulesSections.directive('ruleSections', ['$compile', '$timeout', '$log', function($compile, $timeout, $log){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
            //create a function that is called after the http request
            function insertSectionContent(){
                //template to inject
                var template = '<div ng-repeat="section in tree" ng-include="\'/static/html/rules/text/rule-section.html\'"></div>';
                //compile and inject into element
                element.append($compile(template)($scope));

                //test that manually injects divs
                /*var template = [];
                function createSection(section){
                    template.push('<div class="rule-section'
                        + ' tier-' + section.tier
                        + ' section-type-' + section.type
                        + '"'
                        + 'id="' + section.topParent + '_' + section.slug + '"'
                        + '>');
                    if(section.type == "ex") template.push('<i class="material-icons">help_outline</i>');
                    if(section.type == "i") template.push('<i class="material-icons">info_outline</i>');
                    template.push('<div class="section-title">' + section.title + '</div>');
                    template.push('<div class="section-content">' +section.content + '</div>');
                    for (var j = 1; j < section.children.length; j++){
                        createSection(section.children[j]);
                    }
                    template.push('</div>')
                }

                for (var i = 0; i < $scope.tree.length; i++) {
                    createSection($scope.tree[i]);
                }*/


                //create function to run after compilation
                var after = function() {
                    //make it set itself to the end
                    setTimeout(function () {
                        //if it doesn't detect that the rules are done loading, it ends itself and calls itself again with
                        //a delay of $scope.retryTime
                        if ($('.rule-section').length < 0) {
                            after();
                            return
                        }
                        //otherwise, run the sectionsLoaded js
                        sectionsLoaded();
                        //fade in the rules text, and fade out the loader
                        $('.rules-text').fadeIn($scope.fadeTime);
                        $('#content-loader').find('.preloader-wrapper').each(function(){
                            //after it disappears, remove active to disable it and fadeIn so it can be used again
                            $(this).fadeOut($scope.fadeTime, function(){$(this).removeClass('active').fadeIn();});
                        });
                    }, $scope.retryTime);
                };
                //run the after function
                after();
            }

            //get the tree, and run insertSectionContent as a callback
            $scope.getTree(insertSectionContent);
        };

        return {
            restrict: 'A',
            link: linkFunction
        }
    }]);

    rulesSections.directive('ruleBookmarks', ['$log', '$compile', function($log, $compile){
        //create link function
        var linkFunction = function ($scope, element, attrs){
            //create function to run after http request
            function insertSectionBookmarks(){
                //create template to inject into element
                var template = '<li class="bookmark-tier-{{section.tier}}" ng-repeat="section in tree" ng-include="\'/static/html/rules/text/rule-bookmark.html\'" ng-if="section.type != \'ex\' && section.type != \'i\' && section.type != \'s\'"></li>';
                //compile and inject into element
                element.append($compile(template)($scope));

                //create a function to run after compilation
                var after = function(){
                    //set itself to end of queue
                    setTimeout(function(){
                        //if it doesn't detect that the bookmarks menu is done, end current function and call itself
                        //again with a delay of $scope.retryTime
                        if ($('.bookmarks-menu').find('a').length < 100) {
                            after();
                            return
                        }
                        //otherwise, run the js
                        bookmarksLoaded();
                        //fade in info, fade out loader - disable and fade in loader after it disappears
                        $('.bookmarks-menu').fadeIn($scope.fadeTime);
                        $('#left-menu-loader').find('.preloader-wrapper').each(function(){
                            $(this).fadeOut($scope.fadeTime, function(){$(this).removeClass('active').fadeIn();});
                        });
                    }, $scope.retryTime);
                };

                //run the after function
                after();
            }

            //get the tree, calling insertSectionBookmarks after it's done
            $scope.getTree(insertSectionBookmarks);
        };

        return {
            restrict: 'A',
            link: linkFunction
        }
    }]);
})();