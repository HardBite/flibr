      $(document).ready(function(){
          
          $(".deleteLink").click(function(event){
            //console.log(this);
            event.preventDefault();
            var requestUrl = $(this).attr('href');
            var parentText = $(this).parent().text();
            parentText = parentText.substr(0, (parentText.length-6));
            //console.log(requestUrl);
            //console.log(parentText)
            if(confirm(("Delete "+parentText+". Are you sure?"))){
              $.ajax({
                type: "DELETE",
                url: requestUrl,
                data: "no data required",
                success: function(response){
                  $(".notification").html(response.notification);
                  $(".notification").show()
                  var classToHide = response.class_to_hide
                  //console.log(classToHide)
                  $(classToHide).fadeOut('slow', function(){$(this).remove();})
                }
              })};
          });
            $(".edit").click(function(event){
            //console.log(this);
            event.preventDefault();
            var requestUrl = $(this).attr('href');
            console.log(requestUrl);
            var parentText = $(this).parent().text();
            parentText = parentText.substr(0, (parentText.length-6));
            console.log(parentText);
                                 
            {
              $.ajax({
                type: "GET",
                url: requestUrl,
                data: "no data required",
                success: function(response){
                  var classToSub = response.ClassToSub
                  console.log(response.html)
                  $(classToSub).replaceWith(response.html)
                }
              })};
          });
        });
$(".button").on('click', function(event){
            alert('clicked')
            event.preventDefault();
            var data = $(jQuery(".form")).serializeArray();
            var X = $(".hiddenId")
            console.log(this)
            console.log(this).parent()
            console.log(this).parent().parent()
            $(".notification").fadeOut('slow', function(){$(this).hide();})
            var request = $.ajax({
              type: "POST",
              url: "/add_book",
              data: data,
              success: function(response){
                //console.log(response)
                primeValue = response.prime_value 
                relatedValues = response.related_values
                //console.log(primeValue, relatedValues)
                //console.log(response.html)
                $(".notification").html(response.notification);
                $(".notification").show()
                $(".entityTableBody tr:last").after(response.html)}
            });
            return false;
        });