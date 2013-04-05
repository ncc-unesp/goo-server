function create_job() {
    has_files = false;
    $("#files_div>:file").each(function () {
        if (this.files.length > 0)
            has_files = true;
    });
    if (has_files)
        find_dataproxy(upload_files);
    else
        // no files
        post_job([]);
    return false;
}

function upload_files(addr){
    //create a multipart-form, upload and call post_job
    url = addr + "api/v1/dataproxy/objects/?compress&format=json&token=" + get_token();

    $("#submit_upload_bar").show();

    var filesForm = new FormData($("#fake_file_form")[0]);

    n_files = 0;
    $("#files_div>:file").each(function () {
        for (i=0; i < this.files.length; i++) {
            filesForm.append("file-" + n_files, this.files[i]);
            n_files++;
        }
    });
    filesForm.append("name", slugify($("#name")[0].value) + "-input.zip");

    var xhr = new XMLHttpRequest();

    xhr.onerror = function (data) {
            return do_error("File upload error.");
        };

    xhr.onload = function(e) {
        data = $.parseJSON(this.response);
        input_obj = data["resource_uri"];
        if(typeof input_obj == 'undefined')
            return do_error("Error on upload. (No object id found)");
        post_job([input_obj]);
    };

    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            progress = (e.loaded / e.total) * 100;
            $("#submit_upload_bar")[0].value = progress;
            $("#submit_upload_bar").val(progress); // Fallback
        }
    };

    xhr.open('POST', url, true);
    xhr.send(filesForm);
}

function post_job(input_objs) {
    data = {};
    form = $("#submit_form").serializeArray();
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
            return do_error("Error in the server. (Post job failed)");
        },
        success: function(data) {
            var resp = data;
            href("#jobs");
        }
    });
}

function load_applications(){
    $.ajax({
        url: "/api/v1/apps/?token=" + get_token(),
        dataType: "json",
        error: function (data) {
            return do_error("Error getting jobs list.");
        },
        success: function(data) {
            for (i in data["objects"]) {
                app = data["objects"][i];
                $("#apps_select")
                    .append('<option value="'+ app.resource_uri + '">' + app._name + '</option>');
            }
            $("#apps_select").change(load_template);
            $("#apps_select").change();
        }
    });
}

function load_template(){
    //clear previus fields
    $('#application_description').empty();
    $('#application_usage').empty();
    $('#application_optional').empty();
    $('#application_required').empty();
    $('#application_constant').empty();
    $("a.accordion-toggle").first().click();

    app = $("#apps_select")[0].value;

    if (!app) return false;

    $.ajax({
        url: app + "?token=" + get_token(),
        dataType: "json",
        error: function (data) { 
            return do_error("Error getting template.");
        },
        success: function(data) {
            // fill description and usage
            $('#application_description').text(data["_description"]);
            $('#application_usage').text(data["_usage"]);
            // load template
            $('#application_optional').mustache('application_options_template');
            // fill with data
            for (p in data){
                $('input[name="' + p + '"]').val(data[p]);
            }
            // move to correct section and add class
            required = ["name"];
            required = required.concat(data._required_fields.split(","));
            for (p in required) {
                field = required[p].trim();
                group = $('input[name="' + field + '"]').attr("required", true).closest(".control-group");
                $('#application_required').append(group);
            }

            constant = data._constant_fields.split(",");
            for (p in constant) {
                field = constant[p].trim();
                group = $('input[name="' + field + '"]').attr("disabled", true).closest(".control-group");
                $('#application_constant').append(group);
            }

        }
    });
}

function slugify(text) {
    text = text.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
    text = text.replace(/-/gi, "_");
    text = text.replace(/\s/gi, "-");
    return text;
}

function form_add_file(){
    $("#files_div>:file").each(function () {
        if (this.files.length == 0) this.remove();
    });
    $("#files_div").append('<input name="files[]" onChange="form_add_file()" type="file" multiple>');
}
