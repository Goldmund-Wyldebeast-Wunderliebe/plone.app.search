/* The following line defines global variables defined elsewhere. */
/*global jQuery:false*/

(function ($) {

    $(function () {

        var container, data;
        container = $('#search-results');

        $('#search-filter input.searchPage[type="submit"]').hide();

        function updateResults(data) {
            var str, struct;
            $.ajax({
                url: '@@updated_search',
                data: data,
                success: function (data) {
                    container.hide();
                    container.html(data);
                    $(container).fadeIn('medium');
                    $('#search-term').text(function () {
                        str = $('#updated-search-term').text();
                        $('#updated-search-term').remove();
                        return str;
                    });
                    $('#search-results-number').text(function () {
                        str = $('#updated-search-results-number').text();
                        $('#updated-search-results-number').remove();
                        return str;
                    });
                    $('#search-results-bar #sorting-options').html(
                        function () {
                            struct = $('#updated-sorting-options').html();
                            $('#updated-sorting-options').remove();
                            return struct;
                        }
                    );
                },
                error: function (req, error) {
                    return true;
                }
            });
        }

        $('form.searchPage').submit(function () {
            data = $('form.searchPage').serialize();
            $(container).fadeOut('fast');
            updateResults(data);
            return false;
        });

        $('#search-filter input, #search-filter select').bind('change', 
            function () {
                data = $('form.searchPage').serialize();
                $(container).fadeOut('fast');
                updateResults(data);
                return false;
            }
        );

        $('#sorting-options a').live('click', function () {
            if ($(this).attr('rel')) {
                $("form.searchPage input[name='sort_on']").val($(this).attr('rel'));
            }
            else {
                $("form.searchPage input[name='sort_on']").val('');
            }
            data = $('form.searchPage').serialize();
            updateResults(data);
            return false;
        });

    });
}(jQuery));
