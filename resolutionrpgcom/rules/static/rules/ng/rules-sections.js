(function(){
    var rulesSections = angular.module('rules.sections', []);

    rulesSections.controller("SectionsController", ['$http', '$scope', function($http, $scope) {

        //set up content controller stuff
        $scope.data.sections = {};
        $scope.status.sections = {
            dataRequestSent: false,
            dataRetrieved: false,
            loaded: false,
            subContentLoaded: false
        };
        $scope.promises.sections = {};
        $scope.functions.sections = {};

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

        $scope.functions.sections.organize = function(data){
            //set vars out of loop to reduce process time
            var tier = 0;
            var depth = 0;
            var tree = [];
            var topParent = "";

            //loop through every item
            for (var i = 0; i < data.length; i++){
                //set depth and tier vars
                depth = data[i].depth_string.split('.');
                tier = depth.length;
                //set tier in data
                data[i].tier = tier;
                //set topParent if tier 1
                if (tier == 1) topParent = data[i].title;
                //set all parents regardless of tier (tier 1 will be their own parent)
                data[i].topParent = topParent;

                //if parent, add to top
                if (tier == 1){
                    tree[depth[0]] = sectionData(data[i]);
                }
                //otherwise, use depth list to add a child and send json data
                else {
                    addChild(tree, depth, data[i]);
                }
            }

            //set organized as tree
            $scope.data.sections.organized = tree;
        };

        $scope.functions.sections.injectSkills = function(args){
            if(!args) args = {};
            if(args.time == 'before') {
                //create loading thing for skills
                injectSmallLoader('.skills_skill-list');
            }
            else {
                setTimeout(function(){
                    var start = $('rule-skills');
                    //remove inside of section child
                    $('.skills_skill-list').find('.text-list-container').html('')
                        //then add the table
                        .append(removeHtmlBlockComments($(start).find('.class-table-terse').html()))
                        //then add the list
                        .append(removeHtmlBlockComments($(start).find('.skill-text').html()));
                    //redo scrollspy
                    sectionsScrollSpy();
                }, $scope.retryTime);
            }
        };

        $scope.functions.sections.injectTraits = function(args){
            if(!args) args = {};
            if(args.time == 'before'){
                //create loading thing for skills
                injectSmallLoader('.traits_trait-list');
                injectSmallLoader('.vehicles_vehicle-traits');
            }
            else {
                setTimeout(function(){
                    var start = $('rule-traits');
                    //remove inside of section child
                    $('.traits_trait-list').find('.text-list-container').html('')
                        .append(removeHtmlBlockComments($(start).find('.trait-list-characters').html()));
                    $('.vehicles_vehicle-traits').find('.text-list-container').html('')
                        .append(removeHtmlBlockComments($(start).find('.trait-list-vehicles').html()));
                    //redo scrollspy
                    sectionsScrollSpy();
                }, $scope.retryTime);
            }
        };
    }]);

    rulesSections.directive('ruleSections', ['$rootScope', function($rootScope){
        //write a link function
        var linkFunction = function ($scope, element, attrs){
            $scope.status.active = 'sections';
            //define load function
            $scope.functions.sections.load = function() {
                //start loading, fade, etc
                beginContentLoad($scope.fadeTime);

                var afterLoad = function(){
                    setTimeout(function(){
                        //inject the content, and do fades
                        setRulesContent({
                            pageContent: $('.rules-sections'),
                            leftContent: $('.rules-sections-left'),
                            fadeTime: $scope.fadeTime
                        });
                        //then run the js to hook to current content
                        sectionsLoaded($scope.fadeTime);
                        //make scrollspy happen again on refresh
                        $(document).ready(function(){
                            $(window).resize(sectionsScrollSpy());
                        });

                        //INJECTION of OTHER LOADED CONTENT
                        //only do this if we haven't fully loaded it yet
                        if(!$scope.status.sections.subContentLoaded){
                            $scope.functions.ctrl.get(['skills', 'traits'], {
                                toast: 'Loading lists..',
                                before: {
                                    skills: [$scope.functions.sections.injectSkills, {time: 'before'}],
                                    traits: [$scope.functions.sections.injectTraits, {time: 'before'}]
                                },
                                after: {
                                    skills: $scope.functions.sections.injectSkills,
                                    traits: $scope.functions.sections.injectTraits
                                }
                            });

                            $scope.status.sections.subContentLoaded = true;
                        }

                    }, 0);
                };

                //get the sections
                $scope.functions.ctrl.get('sections', {
                    toast: 'Loading sections...',
                    after: afterLoad
                });
            };

            //define unload function
            $scope.functions.sections.unload = function() {
                //remove scrollspy
                $(window).off("resize", sectionsScrollSpy());
            }
        };

        return {
            restrict: 'E',
            templateUrl: '/static/html/rules/sections/sections.html',
            controller: 'SectionsController',
            controllerAs: 'sections',
            link: linkFunction
        }
    }]);

})();
