'use strict';
{
  const $ = django.jQuery;

  $.fn.djangoAdminSelect2 = function () {
    $.each(this, function (i, element) {
      $(element).select2({
        ajax: {
          data: (params) => {
            let queryParams = {
              term: params.term,
              page: params.page,
              app_label: element.dataset.appLabel,
              model_name: element.dataset.modelName,
              field_name: element.dataset.fieldName
            }
            let prefix = "autocomplete-";

            for (let fieldName in $(element).data()) {
              if (fieldName.startsWith(prefix)) {
                queryParams[fieldName.slice(prefix.length).toLowerCase()] = $(element).data(fieldName);
              }
            }

            return queryParams;
          }
        }, escapeMarkup: function (text) {
          return text;
        },
        templateSelection: function (data, container) {
          if (data.hasOwnProperty("__badge__") && !data.text.startsWith("<a") && container && container.is("li")) {
            data.text = data.__badge__;
          }
          return data.text;
        },
      });
    });
    return this;
  };

  $(function () {
    // Initialize all autocomplete widgets except the one in the template
    // form used when a new formset is added.
    $('.admin-autocomplete').not('[name*=__prefix__]').djangoAdminSelect2();
  });

  document.addEventListener('formset:added', (event) => {
    $(event.target).find('.admin-autocomplete').djangoAdminSelect2();
  });
}
