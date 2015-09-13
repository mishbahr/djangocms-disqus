(function($) {
    $(function() {
        var accountInput = $(':input[name="account"]'),
            syncBtn = $('#sync_shortname');

        syncBtn.on('click', function() {
            getForumsList();
        });
        var getForumsList = function() {
            var accountId = accountInput.val(),
                shortNameInput = $(':input[name="shortname"]'),
                helpText = shortNameInput.parent().siblings('.help'),
                ajaxUrl = syncBtn.data('ajaxUrl');

            helpText.removeClass('error success');

            if (accountId) {
                helpText.html(syncBtn.data('processingMsg'));
                $.getJSON(ajaxUrl, {
                    account: accountId,
                }).done(function(data) {
                    shortNameInput.find('option').remove();
                    $.each(data, function(shortname, name) {
                        shortNameInput.append($('<option/>', {
                            value: shortname,
                            text: name
                        }));
                    });
                    helpText.html(syncBtn.data('completeMsg')).addClass('success');
                }).fail(function(error) {
                    var error = JSON.parse(error.responseText);
                    helpText.html(syncBtn.data('syncError') + ': ' + error.msg).addClass('error');
                });
            } else {
                helpText.html(syncBtn.data('missingAccountMsg')).addClass('error');;
            }
        };
        accountInput.change(function() {
            getForumsList();
        });

        $(':input[name="load_event"]').change(function() {
            var buttonTextField = $('.form-row.field-button_text');
            $(this).val() == 'click' ? buttonTextField.slideDown() : buttonTextField.slideUp();
        }).change();

        $(':input[name="enable_sso"]').change(function() {
            var siteNameField = $('.form-row.field-site_name');
            $(this).is(':checked') ? siteNameField.slideDown() : siteNameField.slideUp();
        }).change();
    });
})(django.jQuery);
