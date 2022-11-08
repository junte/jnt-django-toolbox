'use strict';
{
  const $ = django.jQuery;
  const PREFIX = "autocomplete-";

  const init = function ($element, options) {
    const settings = $.extend({
      ajax: {
        data: function (params) {
          // data-autocomplete-<param>
          // example: data-autocomplete-id

          let queryParams = {
            term: params.term,
            page: params.page,
            app_label: element.dataset.appLabel,
            model_name: element.dataset.modelName,
            field_name: element.dataset.fieldName
          }

          for (let fieldName in $element.data()) {
            if (fieldName.startsWith(PREFIX)) {
              queryParams[fieldName.slice(PREFIX.length).toLowerCase()] = $element.data(fieldName);
            }
          }

          return queryParams;
        }
      },
      escapeMarkup: function (text) {
        return text;
      },
      templateSelection: function (data, container) {
        if (data.hasOwnProperty("__badge__") && !data.text.startsWith("<a") && container && container.is("li")) {
          data.text = data.__badge__;
        }
        return data.text;
      },
    }, options);
    $element.select2(settings);
  };

  $.fn.djangoAdminSelect2 = function (options) {
    const settings = $.extend({}, options);
    $.each(this, function (i, element) {
      const $element = $(element);
      init($element, settings);
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
