$(window).load(function() {
    function bindBtnListener() {
        $(".button").on("click", function(event) {submit(event);});
    };

    function submit(event) {
        event.preventDefault();
        var data = $(jQuery(".form")).serializeArray();
        var request = $.ajax({
            type: "POST",
            url: requestUrl,
            data: data,
            success: function(response) {
                console.log(response)
                $(".notification").html(response.notification);
                $(".notification").show();
                if($(".entityTableBody tr:first").attr('class').indexOf("even") != -1){
                  alert('even is there');
                  (".entityTableBody tr:first").before(response)}
                else{
                  alert('odd is there');
                  response = response.replace('odd', 'even');
                  $(".entityTableBody tr:first").before(response);}
                $("#addForm").addClass("hidden");
                
            }});
    };
    
    console.log('ready');
    
    $("a.add").click(function(event) {
        event.preventDefault();
        console.log('clicked');
        requestUrl = $(this).attr("href");
        console.log(requestUrl);
        $.ajax({
            type: "GET",
            url: requestUrl,
            success: function(response) {
                console.log(response);
                $("#addForm").html(response);
                console.log(this);
                bindBtnListener();
                $("#addForm").removeClass("hidden");
            }
        });
    });
});