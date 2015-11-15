(function () {
    var rulesTables = angular.module('rules.tables', []);

    rulesTables.controller("TablesController", ['$scope', function ($scope) {

        $scope.logo.left.after = 'tables';

        $scope.status.tables = {active: 'none'};
        $scope.functions.tables = {};

        //make a function to format the children for each row
        $scope.functions.tables.formatRowChild = function (args) {
            //set rows html
            var rowsHtml = "";

            //loop through provided rows, making a tr for each row and cells in that row
            for (var obj = 0; obj < args.rows.length; obj++) {
                //initialize classes
                args.rows[obj].classes = args.rows[obj].classes || {};

                //create row
                if (args.rows[obj].classes.row != undefined) {
                    rowsHtml += "<tr class='" + args.rows[obj].classes.row + "'>";
                }
                else rowsHtml += "<tr>";
                for (var cell = 0; cell < args.rows[obj].row.length; cell++) {
                    if (args.rows[obj].classes.cell != undefined) {
                        rowsHtml += "<td class='" + args.rows[obj].classes.cell + "'>";
                    }
                    else rowsHtml += "<td>";
                    //if it's the first cell, assume it's the header
                    if (cell == 0) rowsHtml += args.rows[obj].row[cell];
                    //otherwise, assume it is a data value, and grab the data from that name
                    else rowsHtml += args.data[args.rows[obj].row[cell]];
                    rowsHtml += "</td>";
                }
                rowsHtml += "</tr>";
            }

            //return the rowsHtml in a table format
            return '<div class="row-slider">' +
                '<table>' +
                rowsHtml +
                '</table>' +
                '</div>';
        };

        $scope.functions.tables.formatTable = function (args) {
            if (args.target == 'traits') {
                args.data = $scope.data.traits.raw;
                args.columns = [
                    {title: "Name", data: "name", className: "bold align-left"},
                    {title: "Type", data: "type", className: "filtered-column-select"},
                    {title: "Value", data: "value"},
                    {
                        title: "Short Description",
                        data: "short_description",
                        className: "align-left hide-on-small-and-down"
                    }
                ];
                args.order = [[1, "asc"], [0, "asc"]];
                args.childRows = [
                    {classes: {row: 'hide-on-med-and-up'}, row: ['Short Description', 'short_description']},
                    {row: ['Description', 'description']}
                ];
            }
            else if (args.target == 'skills') {
                args.data = $scope.data.skills.list;
                args.columns = [
                    {title: "Name", data: "name", className: "bold align-left"},
                    {title: "Base Aptitude", data: "base_aptitude"},
                    {title: "Class", data: "skill_class", className: "filtered-column-select"},
                    {title: "What", data: "what", className: "align-left hide-on-med-and-down"}
                ];
                args.order = [[2, "asc"], [0, "asc"]];
                args.childRows = [
                    {classes: {row: 'hide-on-large-and-up'}, row: ['What', 'what']},
                    {row: ['When', 'when']},
                    {row: ['Types', 'types']},
                    {row: ['Specializations', 'specializations']}
                ];
            }
            else if (args.target == 'equipment'){
                args.data = $scope.data.equipment.organized;
                args.columns = [
                    {title: "Name", data: "name", className: "bold align-left"},
                    {title: "Type", data: "category", className: "filtered-column-select"},
                    {title: "Subtype", data: "sub_category", className: "filtered-column-text"},
                    {title: "Cost", data: "cost"},
                    {title: "Short Description", data: "short_description", className: "align-left hide-on-small-and-down"}
                ];
                args.order = [[1, "asc"],[2, "asc"],[0, "asc"]];
                args.childRows = [
                    {classes: {row: 'hide-on-med-and-up'}, row: ['Short Description', 'short_description']},
                    {row: ['Description', 'description']}
                ];
            }

            //make blank order if none provided
            if (args.order == undefined) args.order = [];

            //return the args
            return args;
        }

    }]);

    rulesTables.directive('ruleTables', ['$compile', function ($compile) {
        //write a link function
        var linkFunction = function ($scope, element, attrs) {

            $scope.functions.tables.switch = function (target) {
                //make the page content loader appear
                contentLoaders({begin: true, fadeTime: $scope.fadeTime, leftContent: false});

                //set active
                $scope.status.tables.active = target;

                //just in case args aren't provided - set default
                var args = {target: target};

                //create function to run after we have the data we need
                var switchTable = function () {
                    //format the table based on the args
                    args = $scope.functions.tables.formatTable(args);

                    // TABLE COLUMNS
                    //if there are child rows..
                    if (args.childRows != undefined) {
                        //make a column for showing the child rows
                        args.columns.unshift({
                            className: 'details-control',
                            orderable: false,
                            data: null,
                            defaultContent: '',
                            searchable: false
                        });
                        //add to column number for each item in order to account for new column being added
                        for (var a = 0; a < args.order.length; a++) {
                            args.order[a][0] += 1;
                        }
                    }
                    // END TABLE COLUMNS

                    // SET PAGE CONTENT
                    //create a new, blank table in the page
                    setRulesContent({
                        pageContent: '<div class="input-field"><input id="tables-table-search" type="text">'
                        + '<label for="tables-table-search">Search</label></div>'
                        + '<table id="tables-table" class="table dynamic-table"></table>'
                    });
                    var tableElement = $('#tables-table');
                    var searchElement = $('#tables-table-search');

                    // CREATE DATA TABLE
                    //create the data table using all of the info we have gotten above
                    var table = $(tableElement).DataTable({
                        sDom: '<"dynamic-table-wrapper"t>',
                        paging: false,
                        stateSave: false,
                        data: args.data,
                        order: args.order,
                        columns: args.columns
                    });

                    //CHILD ROW FORMATTING AND SLIDING
                    //if there are child rows..
                    if (args.childRows != undefined) {
                        //add an arrow in the detail control column
                        $('td.details-control').html('<i class="material-icons">keyboard_arrow_down</i>');

                        // Add event listener for opening and closing details
                        $(tableElement).find('tbody').on('click', 'td.details-control', function () {
                            var tr = $(this).closest('tr');
                            var row = table.row(tr);

                            if (row.child.isShown()) {
                                $(this).removeClass('rotated');
                                // This row is already open - close it
                                tr.removeClass('shown');
                                $('div.row-slider', row.child()).slideUp(function () {
                                    row.child.hide();
                                });
                            }
                            else {
                                $(this).addClass('rotated');
                                // Open this row
                                row.child($scope.functions.tables.formatRowChild({
                                    rows: args.childRows,
                                    data: row.data()
                                }), 'no-padding').show();
                                tr.addClass('shown');

                                $('div.row-slider', row.child()).slideDown();
                            }
                        });
                    }
                    // END CHILD ROW FORMATTING AND SLIDING

                    //SORT ICON
                    //create icon to show which way columns are sorted (if at all)
                    $('thead').find('th').append('<i class="sorted material-icons">arrow_drop_down</i>');

                    //COLUMN FILTERS
                    //get columns that we should filter
                    var filteredColumnSelect = $('.filtered-column-select');
                    var filteredColumnText = $('.filtered-column-text');

                    //if there are any filtered columns, create a header and add the filters as necessary
                    if ($(filteredColumnSelect).length + $(filteredColumnText).length > 0) {
                        //create a row for the filters
                        $(tableElement).find('thead').append('<tr id="filter-row"></tr>');

                        //go through columns, add filter if necessary
                        table.columns().every(function () {
                            var column = this;
                            var index = this.index();
                            var thClass = $(this.header()).attr('class');
                            var filter = $('#filter-row').append('<th class="' + thClass + '"></th>').find('th')[index];
                            //if asked to be filtered, go through data
                            if ($(this.header()).hasClass('filtered-column-select')) {
                                //add a select
                                $(filter).append('<select class="select-filter" id="select-filter-' + index + '"><option value="">no filter</option></select>');

                                //sort the data, and add an option for each unique value
                                this.data().unique().sort().each(function (d, j) {
                                    $(filter).find('select').append('<option value="' + d + '">' + d + '</option>');
                                });

                                //name the select item
                                var filterSelect = $('#select-filter-' + index);

                                //make material
                                $(filterSelect).material_select();

                                //when the select value changes, filter the rows
                                $(filterSelect).on('change', function () {
                                    var val = $.fn.dataTable.util.escapeRegex(
                                        $(this).val()
                                    );

                                    column
                                        .search(val ? '^' + val + '$' : '', true, false)
                                        .draw();
                                });
                            }
                            //if it has the text filter
                            else if ($(this.header()).hasClass('filtered-column-text')){
                                //create an input for filtering
                                $(filter).append('<input type="text" id="text-filter-'+index+'">');
                                //save the element
                                var filterText = $('#text-filter-' + index);
                                //on keyup or change, if the search doesn't equal the value, search the value
                                $(filterText).on('keyup change', function(){
                                    if(column.search() !== this.value){
                                        column.search(this.value).draw();
                                    }
                                });
                            }
                        });
                    }
                    //END COLUMN FILTERS

                    //search when you press a key in the searchbar
                    $(searchElement).on('keyup', function () {
                        table.search(this.value).draw();
                    });

                    $('th.filtered-column').find('select').change(function(){console.log('changed a filter')});

                    //fade out the pageContent loaders
                    contentLoaders({begin: false, fadeTime: $scope.fadeTime, leftContent: false});
                };


                //get the data we need, then switch to that table
                $scope.functions.ctrl.get(target, {
                    toast: 'Loading ' + target + '..',
                    after: switchTable
                });
            };

            $scope.functions.tables.load = function () {

                //put loaders for all content
                contentLoaders({begin: true, fadeTime: $scope.fadeTime});
                //compile stuff and put it in left menu
                setTimeout(function(){
                    $('#left-menu-content').html('<div id="tables-left-menu"></div>')
                    .find('#tables-left-menu')
                    .html($compile($('.tables-left-menu').html())($scope));
                }, $scope.fadeTime);
                //fade out left menu loader
                contentLoaders({begin: false, fadeTime: $scope.fadeTime, pageContent: false});

                //call the function to 'switch' to table (create it).. no args mean it will default
                $scope.functions.tables.switch('traits');
            };
        };

        return {
            restrict: 'E',
            controller: 'TablesController',
            templateUrl: '/static/html/rules/tables/tables.html',
            controllerAs: 'tablesCtrl',
            link: linkFunction
        }
    }
    ]);

})();