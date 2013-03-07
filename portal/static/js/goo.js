function goo_first_load() {
    $.Mustache.addFromDom();
    render_login();
    $(window).bind('hashchange', view_change);
    view_change();
};

function view_change() {
    re_hash = location.hash.match("^#([A-Za-z0-9_\-]+)$")
    // no hash
    if (re_hash)
        hash = re_hash[1];
    else
        // default view
        hash = "stats";

    if (hash == "jobs")
        return view_jobs_list();

    re_job_id = hash.match("^job-([0-9]+)$")
    if (re_job_id)
        return view_job_detail(re_job_id[1]);

    // default: try to load hash as template
    render = function () { $('#container').mustache(hash, {}, { method: 'html' })}
    $.Mustache.load(hash + '.html').done(render);
};

function href(anchor){
    location.hash = anchor;
}

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

            $.Mustache.load('jobs.html').done(function () {$('#container').mustache('jobs', resp, { method: 'html' })});
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

            $.Mustache.load('job.html').done(function () {$('#container').mustache('job', resp, { method: 'html' })});
        }})};

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
        do_alert("Missing username");
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
                do_alert("Wrong login/password");
            },
        success: function(data) {
                $.cookie("user", username);
                $.cookie("token", data["token"]);
                render_login();
                view_jobs_list();
            }
        });
    return false;
    };

function do_alert(msg) {
    $(".alert > #msg").html(msg);
    $(".alert").show();
}

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
