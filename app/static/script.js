      $(document).ready(function(){
          $(".button").click(function(event){
            event.preventDefault();
            var data = $(jQuery(".form")).serializeArray();
            $(".notification").fadeOut('slow', function(){$(this).hide();})
            var request = $.ajax({
              type: "POST",
              url: "/json_add_book",
              data: data,
              success: function(response){
                $(".notification").html(response.notification);
                $(".notification").show()}
            });
        });
          $(".deleteLink").click(function(event){
            console.log(this);
            event.preventDefault();
            var requestUrl = $(this).attr('href');
            var parentText = $(this).parent().text();
            parentText = parentText.substr(0, (parentText.length-6));
            console.log(requestUrl);
            console.log(parentText)
            if(confirm(("Delete book"+parentText+". Are you sure?"))){
              $.ajax({
                type: "DELETE",
                url: requestUrl,
                data: "no data required",
                success: function(response){
                  $(".notification").html(response.notification);
                  $(".notification").show()
                  var classToHide = response.class_to_hide
                  console.log(classToHide)
                  $(classToHide).fadeOut('slow', function(){$(this).remove();})
                }
              })};
          });
        });
