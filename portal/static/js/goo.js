function view_jobs_list() {
    $.ajax({
        dataType: "json",
        url: "/api/v1/jobs/?token=" + get_token(),
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
        url: "/api/v1/jobs/"+ id +"/?token=" + get_token(),
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

function view_stats() {
            $.Mustache.load('stats.html').done(function () {$('#container').mustache('stats', {}, { method: 'html' })});
        };

function render_login() {
            $('#login_box').mustache('login_template', {user: get_user()}, { method: 'html' });
        };

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

function do_login() {
    current_user = get_user();
    if (current_user) return current_user;

    username = $("#login_box>input[name=login]")[0].value;
    password = $("#login_box>input[name=password]")[0].value;

    if (username == "") {
        alert("Missing username");
        return;
        }

    $.ajax({
        dataType: "json",
        type: "POST",
        username: username,
        password: password,
        contentType: "application/json", //mandatory
        data: "{}", //mandatory
        url: "/api/v1/auth/",
        error: function(data) {
                alert("Wrong login/password");
            },
        success: function(data) {
                $.cookie("user", username);
                $.cookie("token", data["token"]);
                render_login();
                view_jobs_list();
            }
        });
    };

function do_logout() {
    $.removeCookie("user");
    $.removeCookie("token");
    render_login();
    view_stats();
}

function get_user() {
    // return user login (string) or "undefined"
    return $.cookie("user");
}

function get_token() {
    // return user login (string) or "undefined"
    return $.cookie("token");
}
