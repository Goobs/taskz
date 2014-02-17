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

        $('.message-modal').on('click', function(e){
            var $this = $(this);
            e.preventDefault();

            $.get($this.attr('href'), function(data){
                $('#sendmessage').html(data)
                    .modal('show');
            })
        })

        $(window).on('resize', function(){
            console.log($(window).height())
            $('.chat').height($(window).height() - $('.inputs').outerHeight()-102);
            $('.chat').scrollTop($(document).height())
        }).resize();

    })
})(jQuery)
