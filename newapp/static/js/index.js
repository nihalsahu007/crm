$('document').ready(function(){
	$('.update').click(function(){
		var user_id = $(this).data("id");
		console.log(user_id)
		$.ajax(
			{
				type : "GET",
				url : "/newapp/update/"+user_id,
				success: function(response) {
                      $("#card-body").html(response);
			}
		})
	});
	$('#submit').click(function(){
    	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		var user_id = $("#get-id1").data("id");
        var form=$("form");
        $.ajax(
			{
				type : "POST",
				url : "/newapp/update/"+user_id,
				headers: {'X-CSRFToken': csrftoken},
				data:form.serialize(),
				success: function(data) 
				{
					location.reload()
				}
			})
		});
	});


$('document').ready(function(){
	$('.delete').click(function(){
	confirms=confirm("Are you want to delete record");
		if (confirms==true)
		{
			return true;
		}
		else{
			return false;

		}
	});
});