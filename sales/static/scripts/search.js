$(document).ready(function(){
    $('#search_text').on('input', function(event){
        searched= $('#search_text').val();
        console.log(searched);
    });
});