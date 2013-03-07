function post_job(form) {
    $.ajax({
        dataType: "json",
        type: "POST",
        url: "/api/v1/jobs/?token=" + get_token(),
        data: '{"app":"/api/v1/apps/33/", "args": "10", "executable": "/bin/sleep", "name":"job2" }',
        //data: $(form).serializeArray(),
        contentType: "application/json",
        success: function(data) {
            var resp = data;
        }
    })
    return false;
};
