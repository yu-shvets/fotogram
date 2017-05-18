$('.like').on('click', function(event) {
    event.preventDefault();
    var element = $(this);
    $.ajax({
        url: 'like',
        type: 'GET',
        data: {post_id: element.attr('data-id')},

        success: function(response){
            element.html('Like: ' + response);
        }
    });
});

$('.comment_block').hide();
$('.comment_button').on('click', function () {
    $('#block-' + this.id).toggle();
});


$('.comment_form').on('submit', function(event){
    console.log("form submitted!")  // sanity check
    event.preventDefault();

    var comment = $(this);
    var id = this.id
    console.log("create post is working!") // sanity check
    var formData = comment.serializeArray()
    $.ajax({
        url : comment.attr('action'), // the endpoint
        type : "POST", // http method
        data : formData, // data sent with the post request

        // handle a successful response
        success: function(json){
            console.log(json);
            $('#result-' + id).prepend(json.author + " | " + json.datetime + "<p>" +json.comment+ "</p>"+"<hr>");
            console.log(id)
            comment.each(function(){
            this.reset();
        });
        }
    });
});

