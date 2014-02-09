(function($, undefined){
    $(function(){

        $('.sidebar-toggler').on('click', function(e){
            e.preventDefault();
            $('body').toggleClass('sidebar-hidden');
        })

    })
})(jQuery)
