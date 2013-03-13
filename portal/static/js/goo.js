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
        hash = "home";

    // bind top buttons CSS actions
    $(".navbar-inner li").removeClass("active");
    $(".navbar-inner li a[href=#" + hash + "]").parent().addClass("active");

    if (hash == "jobs")
        return view_jobs_list();

    re_job_id = hash.match("^job-([0-9]+)$")
    if (re_job_id)
        return view_job_detail(re_job_id[1]);

    re_job_id = hash.match("^object-([0-9]+)$")
    if (re_job_id)
        return get_object(re_job_id[1]);

    // default: try to load hash as template
    container_render(hash);
};

function container_render(template, data) {
    // set data default value
    data = data || {};
    render = function () { $('#container').mustache(template, data, { method: 'html' })};
    $.Mustache.load(template + '.html').done(render);
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
            container_render('jobs', resp);
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
            container_render('job', resp);
        }})};

function render_login() {
            $('#login_box').mustache('login_template', {user: get_user()}, { method: 'html' });
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
                href("#jobs");
            }
        });
    return false;
    };

function do_alert(msg) {
    $(".alert > #msg").html(msg);
    $('.alert').fadeIn(1000);
    $('.alert').delay(5000).fadeOut(1000);
}

function do_logout() {
    $.removeCookie("user");
    $.removeCookie("token");
    render_login();
    href("#home");
}

function get_user() {
    // return user login (string) or "undefined"
    return $.cookie("user");
}

function get_token() {
    // return user login (string) or "undefined"
    return $.cookie("token");
}

function get_object(id) {
    //download file from object proxy
    find_dataproxy(function (server) {
        url = addr + "api/v1/dataproxy/objects/"+ id +"/?token=" + get_token();
        window.location = url;
    });
    return false;
}

function find_dataproxy(callback){
    // find a dataproxy server and call upload_files
    // check for cache
    if (typeof goo_dataproxy_server == "undefined") {
        $.ajax({
            type:"GET",
            url: "/api/v1/dataproxyserver/?token=" + get_token(),
            error: function (data) {
                return do_alert("Server error. (Request dataproxy failed)");
            },
            success: function (data) {
                addr = data["objects"][0].url;
                if(typeof addr == 'undefined')
                    return do_alert("Server error. (No data server found)");
                goo_dataproxy_server = addr;
                callback(addr);
            }
        });
    }
    else
        callback(goo_dataproxy_server);
}
