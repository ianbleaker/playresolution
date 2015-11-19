(function () {
    var app = angular.module('rules', [
        'rules.sections',
        'rules.traits',
        'rules.skills',
        'rules.tables',
        'rules.equipment'
    ]);

    app.controller("ContentController", ['$scope', '$http', function ($scope, $http) {
        //logo text
        $scope.logo = {navbar: {}, left: {}};
        $scope.logo.navbar.before = 'rez';
        $scope.logo.navbar.after = 'rules';
        $scope.logo.left.before = 'rules';
        $scope.logo.left.after = 'sections';

        //scope time constants
        $scope.retryTime = 500;
        $scope.fadeTime = 400;

        //containers to track status, promises, functions, data
        $scope.status = {active: ''};
        $scope.promises = {};
        $scope.functions = {};
        $scope.functions.ctrl = {};
        $scope.data = {};

        //watch the active part
        $scope.$watch(function () {
                return $scope.status.active
            },
            function (newValue, oldValue) {
                //if active changes, and new value is real and isn't the same as the old one
                if (newValue != "" && newValue != oldValue) {
                    //if there is an unload function for the old content, run that
                    if (oldValue != "" && $scope.functions[oldValue].unload != undefined) {
                        $scope.functions[oldValue].unload();
                    }
                    //load content based on new value
                    $scope.functions[newValue].load();
                }
            }
        );

        $scope.functions.ctrl.get = function (contentTitles, args) {
            //make a "unique" slug id
            var slug = slugify(JSON.stringify(contentTitles));

            //null args handler
            args = args || {};

            //create load target if it doesn't exist
            args.loadTarget = args.loadTarget || slug;

            //handle before or after being a single function or array (rather than time.all)
            if (args.before != undefined && (typeof args.before == 'function' || args.before.constructor === Array)) args.before = {all: args.before};
            if (args.after != undefined && (typeof args.after == 'function' || args.after.constructor === Array)) args.after = {all: args.after};

            //handle arg being a single function, assume they want 'after.all'
            if (typeof args == 'function') args.after = {all: args};

            //handle string content titles
            if (typeof contentTitles == 'string') contentTitles = [contentTitles];

            //set the load target
            $scope.status.loadTarget = args.loadTarget;

            //set up function runner
            function runner(when, content) {
                //abort if nothing here or if load is targeting new item
                if (!args[when] || $scope.status.loadTarget != args.loadTarget) return;
                //if no content provided, assume "all"
                if (!content) content = 'all';
                //if there is a function for the content provided at the time provided
                if (args[when][content]) {
                    //if it's a function, run it
                    if (typeof args[when][content] == 'function') args[when][content]();
                    //otherwise assume it's an array and run the 0 index with the 1 index as arguments
                    else args[when][content][0](args[when][content][1]);
                }
            }

            //run before all function if it exists
            runner('before');

            //setup success counters
            var success = {all: {count: 0, required: contentTitles.length}};

            //loop to check if everything is loaded
            function isLoaded(content) {
                setTimeout(function () {
                    //set required and counts
                    var required = 1;
                    var count = success[content] || 0;

                    //if no item provided or item is all
                    if (!content || content == 'all') {
                        //set item to all
                        content = 'all';
                        //set success counts and required
                        required = success[content].required;
                        count = success[content].count;
                    }

                    //if data has been received, let the app know
                    if (content != 'all' && $scope.status[content].dataRetrieved) {
                        success.all.count += 1;
                        success[content] = 1;
                    }
                    //if we haven't successfully loaded everything, run this over again with a delay
                    if (count < required) isLoaded(content);
                    //otherwise we're done, run the after stuff
                    else {
                        runner('after', content);
                        //delete toast if need be
                        //uses 'unique' class identifier made before during toast
                        if (args.toast && content == 'all') {
                            $.Velocity($('.' + slug), {"opacity": 0, marginTop: '-40px'}, {
                                duration: 375,
                                easing: 'easeOutExpo',
                                queue: false,
                                complete: function () {
                                    this[0].parentNode.removeChild(this[0]);
                                }
                            });
                        }
                    }
                }, $scope.retryTime * 2);
            }

            //function that gets the content stuff recursively
            function getter() {
                setTimeout(function () {
                    //hold name in var so it can be remembered while the loops occur
                    var content = contentTitles[0];

                    //run function for before this item if it exists
                    runner('before', content);

                    //if the data request hasn't been sent yet
                    if (!$scope.status[content].dataRequestSent) {
                        //tell the app that we have sent the data request
                        $scope.status[content].dataRequestSent = true;
                        //toast if need be - use weird slugged content titles as 'unique' identifier class for toast
                        //toast in this spot means it'll only happen if the data hasn't already been gotten
                        if (args.toast && !args.toasted) {
                            Materialize.toast(args.toast, 99999, slug);
                            args.toasted = true;
                        }
                        //do the promise, save it as the get
                        $scope.promises[content].get = $http.get('json/' + content).then(
                            function (response) {
                                //save the raw data
                                $scope.data[content].raw = response.data;

                                //organize it if we should
                                if ($scope.functions[content].organize) $scope.functions[content].organize(response.data);

                                //tell the app we've retrieved the data
                                $scope.status[content].dataRetrieved = true;

                                //just run the after stuff
                                runner('after', content);

                                //and let the app know we're done with this item
                                success.all.count += 1;
                                success[content] = 1;
                            }
                        );
                    }
                    //if the request has been sent
                    else {
                        //if the data has already been retrieved..
                        if ($scope.status[content].dataRetrieved) {
                            setTimeout(function () {
                                //just run the after stuff
                                runner('after', content);
                                //and let the app know we're done with this item
                                success.all.count += 1;
                                success[content] = 1;
                            }, 0);
                        }
                        //if data hasn't been received yet
                        else {
                            //loop over it to see if it is loaded
                            isLoaded(content);
                        }
                    }

                    contentTitles.shift();
                    //if there are items left, run this again
                    if (contentTitles[0] != null) getter();
                }, $scope.retryTime);
            }

            getter();
            isLoaded('all');
        };

        $scope.functions.ctrl.organizeByCategory = function (data, categoryName) {
            var outputObject = {};
            for (var i = 0; i < data.length; i++) {
                if (!outputObject[data[i][categoryName]]) {
                    outputObject[data[i][categoryName]] = {};
                    outputObject[data[i][categoryName]].name = data[i][categoryName];
                    outputObject[data[i][categoryName]].content = [];
                }
                outputObject[data[i][categoryName]].content.push(data[i]);
                outputObject[data[i][categoryName]].content.sort(function (a, b) {
                    return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);
                });
            }

            var output = [];
            for (var index in outputObject) {
                if (outputObject.hasOwnProperty(index)) {
                    output.push(outputObject[index])
                }
            }
            output.sort(function (a, b) {
                return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);
            });

            return output;
        }

    }]);

    //create a filter to allow binding to raw html
    app.filter('rawHtml', ['$sce', function ($sce) {
        return function (val) {
            return $sce.trustAsHtml(val);
        };
    }]);

})();
