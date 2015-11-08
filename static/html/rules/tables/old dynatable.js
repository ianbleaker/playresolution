var rowWriter = function (rowIndex, record, columns, cellWriter) {
    var tr = '';

    // grab the record's attribute for each column
    for (var i = 0, len = columns.length; i < len; i++) {
        tr += cellWriter(columns[i], record);
    }

    return '<tr class="dyn-row">' + tr + '</tr>';
};

var dynatable = $('#traits-table').find('table').dynatable({
    features: {
        paginate: false,
        perPageSelect: false,
        recordCount: false,
        pushState: false,
        search: false
    },
    dataset: {
        records: $scope.data.traits.raw
    },
    inputs: {
        queries: $('#search')
    },
    table: {
        defaultColumnIdStyle: 'underscore',
        bodyRowSelector: 'tbody tr.dyn-row',
        copyHeaderClass: true
    },
    writers: {
        _rowWriter: rowWriter
    }
}).data('dynatable');
$('select').material_select();

$('.table-filter').each(function () {
    $(this).change(function () {
        var value = $(this).val();
        var key = $(this).attr('name');
        if (value === "") {
            dynatable.queries.remove(key);
        } else {
            dynatable.queries.add(key, value);
        }
        dynatable.process();
    });
});

$('.dyn-row').hover(
    function () {
        $(this).addClass('hover')
    },
    function () {
        $(this).removeClass('hover')
    }
);