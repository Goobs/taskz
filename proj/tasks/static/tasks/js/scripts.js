(function($, undefined){
    $(function(){

        $('.sidebar-toggler').on('click', function(e){
            e.preventDefault();
            $('body').toggleClass('sidebar-hidden');
        })

        $('.add-form').on('click', function(e){
            e.preventDefault();
            $('.dynamic-form').slideDown();
            $('.add-form').hide()
        })

        $('.delete-form').on('click', function(e){
            e.preventDefault();
            $('.dynamic-form').slideUp();
            $('.add-form').show();
        })

    })
})(jQuery)
