function get_jobs_list(token, success) {
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

            success(resp);
        }})}
