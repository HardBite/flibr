$(window).load(function() {
    var requestUrl = ""

    function bindBtnListener() {
        console.log('bindBtnListener call recieved');
        $(".button").on("click", function(event) {submit(event)})
    };

    function bindLinkListener() {
        console.log('bindLinkListener call recieved');
        $("a.edit").on("click", function(event) {edit(event)});
    };

    function submit(event) {
        event.preventDefault();
        var data = $(jQuery(".form")).serializeArray();
        console.log(data)
        console.log('in submit function'+requestUrl)
        var request = $.ajax({
            type: "POST",
            url: requestUrl,
            data: data,
            success: function(response) {
                //console.log(response)
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
    
    function edit(event){
        event.preventDefault();
        console.log(event)
        requestUrl = event.target.href
        console.log(requestUrl)
        splittedUrl = requestUrl.split('/');
        console.log(splittedUrl)
        var classToSub = '.row_'+splittedUrl[(splittedUrl.length -1 )]
        console.log(classToSub)

            $.ajax({
            type: "GET",
            url: requestUrl,
            data: "no data required",
            success: function(response){
               console.log(response)
              $(classToSub).replaceWith('<tr class ='+classToSub+'> <td>'+response+'</td> </tr>')
              bindBtnListener()
            }});
      
    };
    
    console.log('ready');
    bindLinkListener();
    
    $("a.add").click(function(event) {
        event.preventDefault();
        console.log('clicked');
        requestUrl = $(this).attr("href");
        //console.log(requestUrl);
        $.ajax({
            type: "GET",
            url: requestUrl,
            success: function(response) {
                //console.log(response);
                $("#addForm").html(response);
                //console.log(this);
                bindBtnListener();
                $("#addForm").removeClass("hidden");
            }
        });
    });


});