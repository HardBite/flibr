$(window).load(function() {
    var requestUrl = ""
    var selectorToSub = ""
        //Hide add book and add author links in navbar
    $("a.add").addClass("hidden")
        //Show button to add new entry in top of the index table
    $("#addNew").removeClass("hidden")

    /*Ensures that alternating rows has corresponding classes to
    maintain them "zebra"-coloured*/
    function rezebrize() {
        console.log("rezebrize call recieved");
        $('tbody > tr:even').removeClass('even odd').addClass('even')
        $('tbody > tr:odd').removeClass('even odd').addClass('odd')
    };

    //Recives a call whenever buttons dynamically added to bind event to them
    function bindBtnListener() {
        console.log('bindBtnListener call recieved');
        $("#submit").off().on("click", function(event) {
            submitNew(event)
        });
        $("#cancel").off().on("click", function(event) {
            cancel(event)
        });
    };

    //Recives a call whenever links dynamically added to bind event to them
    function bindLinkListener() {
        console.log('bindLinkListener call recieved');
        $("#addNew").off().on("click", function(event) {
            addObject(event, $(this).data('ref'))
        });
        $("a.edit").off().off().on("click", function(event) {
            editObject(event, $(this).parent().parent().attr('class'))
        });
        $("a.delete").off().on("click", function(event) {
            deleteObject(event, $(this).parent().parent().attr('class'))
        })
    };
    //Adds cancel button to dynamically added forms
    function addCancelButton() {
        $("#buttons").append('<input type="button" id="cancel" value="Cancel" >')
    };


    function submitNew(event) {
        console.log('submmit button clicked')
        event.preventDefault();
        var data = $(jQuery(".form")).serializeArray();
        console.log(data)
        console.log('in submit function' + requestUrl)
        var request = $.ajax({
            type: "POST",
            url: requestUrl,
            data: data,
            success: function(response) {
                console.log(response)
                error = response.error
                if (error) {
                    $("div.notification").html(error)
                } else {

                    //$(".entityTableBody tr:first").after(response);
                    
                    $("#addNew").removeClass("hidden")
                    console.log("Submit New is going to replace" + selectorToSub)
                    $(selectorToSub).replaceWith(response)
                    $(".form").parent().parent().remove()
                    rezebrize()
                    bindLinkListener()
                    bindBtnListener()
                }
            }

        });
    };

    function editObject(event, element_class) {
        console.log('editObject call recieved')
        event.preventDefault();
        requestUrl = event.target.href;
        selectorToSub = '.' + element_class.split(' ').join('.')
        console.log(selectorToSub);
        $.ajax({
            type: "GET",
            url: requestUrl,
            success: function(response) {
                console.log(response.length)
                $(selectorToSub).hide()
                $(selectorToSub).after('<tr><td>' + response + '</td></tr>');
                addCancelButton()
                bindBtnListener()
                //bindLinkListener()
                rezebrize()
            }
        });
    };

    rezebrize()
    console.log('ready');
    bindLinkListener();

    function addObject(event, data) {
        event.preventDefault();
        console.log('add object clicked');
        console.log(data)
            //requestUrl = $(this).attr("href");
        requestUrl = data
        selectorToSub = "#replaceMe"
        console.log(requestUrl);
        $.ajax({
            type: "GET",
            url: requestUrl,
            success: function(response) {
                console.log(response.length);
                $("tbody tr:first").before("<tr id='replaceMe'> <td>"+response+" </td></tr>")
                $("#addNew").addClass("hidden");
                addCancelButton();
                bindBtnListener();
                rezebrize();

            }
        });
    };

    function cancel(event) {
        console.log('cancel clicked')
        $(".form").parent().parent().remove();
        $("#addNew").removeClass("hidden");
        $(selectorToSub).show();
        rezebrize();


    };


    function deleteObject(event, element_class) {
        event.preventDefault();
        requestUrl = event.target.href;
        console.log(requestUrl);
        selectorToSub = '.' + element_class.split(' ').join('.')
        $.ajax({
            type: "DELETE",
            url: requestUrl,
            success: function(response) {
                $(".notification").html(response.notification);
                $(".notification").show()
                $(selectorToSub).fadeOut('slow', function() {
                    $(this).remove();
                    rezebrize();
                });
                
            }
        });
    };


});