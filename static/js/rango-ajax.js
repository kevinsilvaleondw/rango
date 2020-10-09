$(document).ready(function() {
    $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
         $.get('/rango/like_category/', {category_id: catid}, function(data){
                   $('#like_count').html(data);
                   $('#likes').hide();
               });
    });// JQuery code to be added in here.

    $('#suggestion').keyup(function(){
            var query;
            query = $(this).val();
            $.get('/rango/suggest_category/', {suggestion: query}, function(data){
             $('#cats').html(data);
            });
    });
});