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
    if (re_job_id) {
        get_object(re_job_id[1]);
        history.back();
        return false;
    }

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

function create_paginator(meta) {
    paginator = [];

    total = meta["total_count"];
    limit = meta["limit"];
    offset = meta["offset"];
    pages = total / limit;
    current = offset/limit;

    c="enabled";
    if (current == 0)
        c="disabled";
    item = ["Previous", (current-1)*limit, limit, c];
    paginator.push(item);

    plus = 3;
    if ((current - plus) >0 ) {
        item = ["...", 0, limit, "enabled"];
        paginator.push(item);
    }

    for (i=current-plus; i<current+plus; i++) {
        if ((i >= 0) && (i < pages)) {
            c="enabled";
            if (i == current)
                c="active";
            item = [i+1, i*limit, limit, c];
            paginator.push(item);
        }
    }

    if ((current + plus) < pages ) {
        item = ["...", total-limit, limit, "enabled"];
        paginator.push(item);
    }

    c="enabled";
    if (current == pages-1)
        c="disabled";
    item = ["Next", (current+1)*limit, limit, c];
    paginator.push(item);

    return paginator;
}

function view_jobs_list(offset, limit) {
    append = '';
    if (typeof offset != "undefined")
        append += "&offset=" + offset;
    if (typeof limit != "undefined")
        append += "&limit=" + limit;

    $.ajax({
        dataType: "json",
        url: "/api/v1/jobs/?token=" + get_token() + append,
        success: function(data) {
            var resp = {};
            resp["jobs"] = data["objects"];
            resp["total"] = data["meta"]["total_count"];
            resp["paginator"] = create_paginator(data["meta"]);
            resp.status_name = function() {
                if (this["status"] == "C") return "Completed";
                if (this["status"] == "P") return "Pending";
                if (this["status"] == "E") return "Error";
                return this["status"];
            };
            container_render('jobs', resp);
        }})

    return false;
};


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
                server = data["objects"][0];
                if(typeof server == 'undefined')
                    return do_alert("Server error. (No data server found)");
                addr = server.url
                goo_dataproxy_server = addr;
                callback(addr);
            }
        });
    }
    else
        callback(goo_dataproxy_server);
}
