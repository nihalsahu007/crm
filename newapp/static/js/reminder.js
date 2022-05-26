$('document').ready(function(){
	$('.done_button').click(function(){
		var reminder_id = $("#get-id").data("id");
		console.log(reminder_id)
		$.ajax({
				type : "GET",
				url : "/newapp/follow_up/"+reminder_id,
				success: function(data) 
				{
					if(data == 'Success True' )
					{
						$( '#message' ).text(data);
						setTimeout(() => window.location.reload(), 2000);
					}
			
        		}
        	})
	});
	
	$('.update').click(function(){
		var reminder_id = $('#get-id1').data("id");
		console.log(reminder_id)
		$.ajax({
			type : "GET",
			url : "/newapp/update_reminder/"+reminder_id,
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
				url : "/newapp/update_reminder/"+user_id,
				headers: {'X-CSRFToken': csrftoken},
				data:form.serialize(),
				success: function(data)
				{
					location.reload()
				}
			})

		});
	
	});

// });