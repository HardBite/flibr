$(window).load(function() {
    var requestUrl = ""
    var selectorToSub = ""

    $("a.add").addClass("hidden")
    $("#addNew").removeClass("hidden")

    function rezebrize() {
        console.log("rezebrize call recieved");
        $('tbody > tr:even').removeClass('even odd').addClass('even')
        $('tbody > tr:odd').removeClass('even odd').addClass('odd')
    };
    

    function bindBtnListener() {
        console.log('bindBtnListener call recieved');
        $("#submit").on("click", function(event) {submitNew(event)})
    };

    function bindLinkListener() {
        console.log('bindLinkListener call recieved');
        $("#addNew").on("click", function(event) {addObject(event, $(this).data('ref'))});
        $("a.edit").on("click", function(event) {editObject(event, $(this).parent().parent().attr('class'))});
        $("a.delete").on("click", function(event) {deleteObject(event, $(this).parent().parent().attr('class'))})
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
                //$(".entityTableBody tr:first").after(response);
                $("#addForm").addClass("hidden");
                console.log("Submit New is going to replace" + selectorToSub)
                $(selectorToSub).replaceWith(response)
                rezebrize()
                bindLinkListener()
                bindBtnListener()}
                             
            });
    };
    
    function editObject(event, element_class){
        console.log('editObject call recieved')
        event.preventDefault();
        console.log(event);
        requestUrl = event.target.href;
        console.log(requestUrl);
        selectorToSub = '.'+element_class.split(' ').join('.')
        console.log(selectorToSub);
        //$(selectorToSub).fadeOut('slow', function() {$(this).remove()});
        
            $.ajax({
            type: "GET",
            url: requestUrl,
            success: function(response){
                console.log(response)
              $(selectorToSub).html('<td>' + response + '</td>');
              //$(selectorToSub).remove()
              //selectorToSub = "#tempRow"
              console.log(selectorToSub)
              bindBtnListener()
              bindLinkListener()
              rezebrize()
            }});
    };
    
    rezebrize()    
    console.log('ready');
    bindLinkListener();
    
    function addObject(event, data) {
        event.preventDefault();
        console.log('clicked');
        console.log(data)
        //requestUrl = $(this).attr("href");
        requestUrl = data
        console.log($("#replaceMe").length)
        if($("#replaceMe").length){}
        else{$("#addForm").parent().parent().after("<tr id='replaceMe'> </tr>")}
        selectorToSub = "#replaceMe"
        console.log(requestUrl);
        $.ajax({
            type: "GET",
            url: requestUrl,
            success: function(response) {
                console.log(response);
                $("#addForm").html(response);
                //console.log(this);
                bindBtnListener();
                $("#addForm").removeClass("hidden");
            }
        });
    };

    function deleteObject(event, element_class){
        event.preventDefault();
        requestUrl = event.target.href;
        console.log(requestUrl);
        selectorToSub = '.'+element_class.split(' ').join('.')
        $.ajax({
                type: "DELETE",
                url: requestUrl,
                success: function(response){
                  $(".notification").html(response.notification);
                  $(".notification").show()
                  $(selectorToSub).fadeOut('slow', function(){$(this).remove();})
                }
              });
    };


});