function likeHandler() {
    var articleDiv = $(this).parent();
    var articleId = articleDiv.attr('id');
    $.ajax({
        url: '/articles/' + articleId + '/addlike/', // articles/3/addlike/
        data: null
    }).done(function(data) {
        articleDiv.find('.likes').text(data.count);
    }).fail(function(){
        alert('Failed!');
    });
}

function comment_likeHandler() {
    var commentDiv = $(this).parent();
    var commentId = commentDiv.attr('id');
    var articleDiv = $(this).parent().parent();
    var articleId = articleDiv.attr('id');

    $.ajax({
        url: '/articles/' + articleId + '/comments/' + commentId + '/addlike/', // articles/3/addlike/
        data: null
    }).done(function(data) {
        commentDiv.find('.likes').text(data.count);
    }).fail(function(){
        alert('Failed!');
    });
}

$('.like_comment').on('click', comment_likeHandler);
$('.like').on('click', likeHandler);

