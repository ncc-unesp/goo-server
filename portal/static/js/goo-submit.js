function create_job() {
    if ($('#inputFiles')[0].files.length)
        find_dataproxy();
    else
        // no files
        post_job([]);
    return false;
}

function find_dataproxy(){
    //find a dataproxy server and call upload_files
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
            upload_files(addr);
        }
    });
}

function upload_files(addr){
    //create a multipart-form, upload and call post_job
    //var filesForm = new FormData($('inputFiles')[0]);
    var filesForm = new FormData();
    filesForm.append("files", $('#inputFiles')[0]);
    filesForm.append("name", slugify($("#name")[0].value) + "-input.zip");
    $.ajax({
        type:"POST",
        url: addr + "api/v1/dataproxy/objects/?compress&token=" + get_token(),
        // Form data
        data: filesForm,
        dataType: "json",
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false,
        error: function (data) {
            return do_alert("File upload error.");
        },
        success: function (data) {
            input_obj = data["resource_uri"];
            if(typeof input_obj == 'undefined')
                return do_alert("Error on upload. (No object id found)");
            post_job([input_obj]);
        }
    });
}

function post_job(input_objs) {
    data = {};
    form = $("#submit_form").serializeArray()
    for (i in form)
        data[form[i].name] = form[i].value;

    data["input_objs"] = input_objs;
    $.ajax({
        type: "POST",
        url: "/api/v1/jobs/?token=" + get_token(),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        //data: $(form).serializeArray(),
        contentType: "application/json",
        error: function (data) { 
            return do_alert("Error in the server. (Post job failed)");
        },
        success: function(data) {
            var resp = data;
            href("#jobs");
        }
    });
}

function slugify(text) {
    text = text.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
    text = text.replace(/-/gi, "_");
    text = text.replace(/\s/gi, "-");
    return text;
}
