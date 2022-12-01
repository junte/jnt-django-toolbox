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
            app_label: $element[0].dataset.appLabel,
            model_name: $element[0].dataset.modelName,
            field_name: $element[0].dataset.fieldName
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
    /*
    * Hacky fix for a bug in select2 with jQuery 3.6.0's new nested-focus "protection"
    * see: https://github.com/select2/select2/issues/5993
    * see: https://github.com/jquery/jquery/issues/4382
    *
    * TODO: Recheck with the select2 GH issue and remove once this is fixed on their side
    */
    $element.on('select2:open', function (e) {
      const searchInput = $element.data('select2').$dropdown.find('.select2-search__field')[0];
      if (searchInput) {
        searchInput.focus();
      }
    });
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
