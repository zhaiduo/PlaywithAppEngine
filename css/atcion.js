

$(document).ready(function(){
   $('.msg').click(function() {
     var idstr=$(this).attr('id');
	 $('#msg1').html($('#'+idstr).text());
	 $("#msg1").fadeIn("slow");
   });
    $('#clear_all').click(function() {
	  if(confirm('Are you sure to clear all?')){
        $.ajax({
		   type: "POST",
		   url: "/ajax_delall",
		   data: "clear=1",
		   error: function(msg){
             alert('Error to delete all msgs.');
		   },
		   success: function(msg){
			 if(msg.match(/^ok$/i)){
                $('.entry').hide();
			 }else{
				alert('Failed to delete all msgs.');
			 }
		   }
		 });
	  }
   });

   
   $('.del').click(function() {
     var idstr=$(this).attr('id');
	 if(idstr.match(/^del_([0-9]+)$/i)){
       var id=RegExp.$1;
	   if($('#entry_'+id)){
		if(confirm('Are you sure to delete this?')){
         $.ajax({
		   type: "GET",
		   url: "/ajax_delete",
		   data: "id="+id,
		   error: function(msg){
             alert('Error to delete a msg.');
		   },
		   success: function(msg){
			 if(msg.match(/^ok$/i)){
                $('#entry_'+id).hide();
			 }else{
				alert('Failed to delete msg.');
			 }
		   }
		 });
		}
	   }
	 }
   });
});

