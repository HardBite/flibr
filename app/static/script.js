$(window).load(function() {
    var requestUrl = ""
    var selectorToSub = ""

    $("a.add").addClass("hidden")
    $("#addNew").removeClass("hidden")


    function bindBtnListener() {
        console.log('bindBtnListener call recieved');
        $("#submit").on("click", function(event) {submitNew(event)})

    };

    function bindLinkListener() {
        console.log('bindLinkListener call recieved');
        $("#addNew").on("click", function(event) {addObject(event, $(this).data('ref'))});
        $("a.edit").on("click", function(event) {editObject(event)});
    };

    function submitNew(event) {
        console.log('submmit button clicked')
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
                if($(".entityTableBody tr:nth-child(2)").attr('class').indexOf("even") != -1){
                  alert('even is there');
                  $(".entityTableBody tr:first").after(response);}
                else{
                  alert('odd is there');
                  response = response.replace('odd', 'even');                  
                  $(".entityTableBody tr:first").after(response);}
                $("#addForm").addClass("hidden")
                             
            }});
    };
    
    function editObject(event){
        event.preventDefault();
        console.log(event);
        requestUrl = event.target.href;
        console.log(requestUrl);
        splittedUrl = requestUrl.split('/');
        console.log(splittedUrl);
        var selectorToSub = '.row_'+splittedUrl[(splittedUrl.length -1 )];
        console.log(selectorToSub);
        
            $.ajax({
            type: "GET",
            url: requestUrl,
            data: "no data required",
            success: function(response){
               console.log(response)
              $(selectorToSub).replaceWith('<tr class ='+selectorToSub+'> <td>'+response+'</td> </tr>')
              bindBtnListener()
            }});
      
    };
    
    console.log('ready');
    bindLinkListener();
    
    function addObject(event, data) {
        event.preventDefault();
        console.log('clicked');
        console.log(data)
        //requestUrl = $(this).attr("href");
        requestUrl = data
        
        selectorToSub = "#addForm"
        console.log(requestUrl);
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
    };


});