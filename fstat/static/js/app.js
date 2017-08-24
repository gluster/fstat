(function () {
    $('input[name="daterange"]').daterangepicker({
    locale: {format: "YYYY-MM-DD"},
    }, function(start, end, label) {
        start = start.format('YYYY-MM-DD');
        end = end.format('YYYY-MM-DD');
        var location = window.location.toString().split("?")[0];
        window.location = location + `?start_date=${start}&end_date=${end}`;
    });

    function hasNaN(array) {
        for (let i = 0; i < array.length; i++) {
            if (isNaN(array[i])) {
                return true;
            }
        }
        return false;
    }
    listeners = {
        showModal: function(fid, bugs) {
            failure_id = fid
            $('#associate-bug-modal').modal('show');
            $('#bugIds').val(bugs);
            $('#bugIds').tagsinput();
        },
        submit: function() {
                var bugIds = $('#bugIds').val().split(',').map(function(bugId){return parseInt(bugId)});
                if (!hasNaN(bugIds) || $('#bugIds').val() == '') {
                    var URL = `/associate-bugs/${failure_id}`;
                    $.ajax({
                        url: URL,
                        beforeSend: function(xhr){
                            xhr.setRequestHeader("Content-Type","application/json");
                        },
                        data: JSON.stringify({bugIds: bugIds}),
                        type: 'POST',
                        success: function(data, status, xhr){
                            location.reload();
                        },
                        error: function(err, status, xhr){
                            showSnackBar(err.response, 3000);
                        }
                    });
                } else {
                    showSnackBar("All bugs must be numbers.", 3000);
                }
        }
    };
}());
