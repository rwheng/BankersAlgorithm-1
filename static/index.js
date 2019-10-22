// Collect the current configuration for resetting
let base_config = $("#txt_config").val();
let current_config = base_config

// Assign a handler to the reset to default button that will reset the
// current configuration to the default
$("#btn_reset_config").on("click", () => {
	$("#txt_config").val(base_config);
	update_config();
});

// Assign a handler to the submit config button that pings the
// flask server with the updated configuration and parses the response
$("#btn_update_config").on("click", update_config);

function update_config() {
	current_config = JSON.stringify({config: parse_configuration($("#txt_config").val())});
	$.ajax({
		type: "POST",
		url: "/update",
		data: {config: current_config},
		dataType: "json",
        success: function(data){
        	console.log(data);
        },
        failure: function(errMsg) {
            console.err(errMsg);
        }
	});
}

function pulldown_config() {
	let remote_config = {}
	$.ajax({
		type: "GET",
		url: "/current",
        success: function(data){
        	remote_config = data;

        	let config_as_txt = remote_config["num_proc"].toString() + "\n" +
						remote_config["num_res"].toString() + "\n" + 
						remote_config["resources"].join(" ") + "\n";

			for(let i = 0; i < remote_config["allocation"].length; i++) {
				config_as_txt += remote_config["allocation"][i].join(" ");
				config_as_txt += "\n";
			}

			for(let i = 0; i < remote_config["max"].length; i++) {
				config_as_txt += remote_config["max"][i].join(" ");
				config_as_txt += "\n";
			}

			config_as_txt.slice(0, config_as_txt.length - 1);
			current_config = config_as_txt;
			$("#txt_config").val(current_config);
        },
        failure: function(errMsg) {
            console.err(errMsg);
        }
	});
}
	

// Assign a handler to the resource request button that pings the flask
// server with the request and parses the response
$("#btn_submit_request").on("click", () => {
	let proc_id = parseInt($("#txt_process_id").val())
	let resource_req = $("#txt_resource_request").val().split(" ").map(parseFloat);
	console.log({proc_id: proc_id, resource_req: resource_req})
	$.ajax({
		type: "POST",
		url: "/request",
		data: {proc_id: proc_id, resource_req: resource_req},
        success: function(data){
        	console.log(data.log);

        	$("#resource_request_log").val(data.log.join("\n"));
        	let alert = ""
        	if (data.is_safe) {
        		alert = generate_safe_alert(data.safe_seq);
        	} else {
        		alert = generate_unsafe_alert();
        	}
    		// $("#div_safety_alert").empty();
    		$("#div_safety_alert").append(alert);

        },
        failure: function(errMsg) {
            console.err(errMsg);
        }
	});
	$("#txt_process_id").val("");
	$("#txt_resource_request").val("")
	pulldown_config();
});

// Assign a handler to check the safety of the system that pings the flask
// server with the request and parses the response
$("#btn_check_safety").on("click", () => {
	$.ajax({
		type: "GET",
		url: "/safety",
        success: function(data){
        	$("#resource_request_log").val(data.log);
        	let alert = ""
        	if (data.is_safe) {
        		alert = generate_safe_alert(data.safe_seq);
        	} else {
        		alert = generate_unsafe_alert();
        	}
    		$("#div_safety_alert").empty();
    		$("#div_safety_alert").append(alert);

        },
        failure: function(errMsg) {
            console.err(errMsg);
        }
	});
});

function parse_configuration(configuration_text) {
	// TODO MAKE SURE IS GOOD
	let split = configuration_text.split("\n");

	let num_proc = parseFloat(split[0]);
	let num_res = parseFloat(split[1]);
	let resources = split[2].split(" ").map(parseFloat);
	let allocation = [];
	let max = []
	for (var i = 0; i < num_proc; i++) {
		allocation.push(split[i + 3].split(" ").map(parseFloat));
		max.push(split[i + 3 + num_proc].split(" ").map(parseFloat));
	}
	
	return {
		num_proc: num_proc,
		num_res: num_res,
		resources: resources,
		allocation: allocation,
		max: max
	};
}

function generate_safe_alert(safe_sequence) {
	return '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
	   	   '<strong>The system is safe!</strong> The safe sequence is ' + safe_sequence.join(", ") +
		   '.<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
	   	   '<span aria-hidden="true">&times;</span>' + 
		   '</button>' +
	       '</div>';
}

function generate_unsafe_alert() {
	return '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
		   '<strong>The system is unsafe!</strong> No sequence of processes will allow the system to run' +
  		   '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
    	   '<span aria-hidden="true">&times;</span>' + 
  		   '</button>' +
		   '</div>';
}