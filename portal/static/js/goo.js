function view_jobs_list() {
    $.ajax({
        dataType: "json",
        url: "http://submit.grid.unesp.br:8000/api/v1/jobs/?token=" + token,
        success: function(data) {
            var resp = {};
            resp["jobs"] = data["objects"];
            resp.status_name = function() {
                if (this["status"] == "C") return "Completed";
                if (this["status"] == "P") return "Pending";
                if (this["status"] == "E") return "Error";
                return this["status"];
            };

            $.Mustache.load('jobs_list.html').done(function () {$('#container').mustache('jobs_list', resp, { method: 'html' })});
        }})};

function view_job_detail(id) {
    $.ajax({
        dataType: "json",
        url: "http://submit.grid.unesp.br:8000/api/v1/jobs/"+ id +"/?token=" + token,
        success: function(data) {
            var resp = data;
            resp.status_name = function() {
                if (this["status"] == "C") return "Completed";
                if (this["status"] == "P") return "Pending";
                if (this["status"] == "E") return "Error";
                return this["status"];
            };

            $.Mustache.load('job_detail.html').done(function () {$('#container').mustache('job_detail', resp, { method: 'html' })});
        }})};

function view_job_submit() {
            $.Mustache.load('job_submit.html').done(function () {$('#container').mustache('job_submit', {}, { method: 'html' })});
        };

function view_graphs() {
            $.Mustache.load('graphs.html').done(function () {$('#container').mustache('graphs', {}, { method: 'html' })});
        };


function post_job(form) {
    $.ajax({
        dataType: "json",
        type: "POST",
        url: "http://submit.grid.unesp.br:8000/api/v1/jobs/?token=" + token,
        data: '{"app":"/api/v1/apps/33/", "args": "10", "executable": "/bin/sleep", "name":"job2" }',
        //data: $(form).serializeArray(),
        contentType: "application/json",
        success: function(data) {
            var resp = data;

            console.log(data);
        }
    })
    return false;
};
