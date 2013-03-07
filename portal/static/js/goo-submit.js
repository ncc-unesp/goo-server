function create_job(form) {
    find_dataproxy();
    return false;
}

function find_dataproxy(){
    //find a dataproxy server and call upload_files

    $.get("/api/v1/dataproxyserver/?token=" + get_token(),
            function (data) {
                addr = data["objects"][0].url;
                upload_files(addr);
            })
}

function upload_files(addr){
    //create a multipart-form, upload and call post_job
    console.log(addr);

    input_obj = "foo";
    post_job(input_obj);
}

function post_job(form) {
    //find dataproxy server
    //upload files and save obj_url
    //port job
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
};
