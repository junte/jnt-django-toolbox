"use strict";

(function ($) {
  const SELECT_ALL = "Select all";
  const UNSELECT_ALL = "Unselect all";

  function addHandlerToFlagsFieldButton() {
    $('button[name="flags_select_all"]').each(function (_, button) {
      const $button = $(button);
      const $elements = $button.nextAll("li");

      $button.on("click", clickButtonHandler);
      $elements.on("change", changeElementsHandler);

      if (isSelectAll($elements)) {
        $(button).text(UNSELECT_ALL);
      }
    });
  }

  function changeElementsHandler(event) {
    let $elements = $(event.target).closest("ul").children("li");
    let $button = $(event.target).closest("li").siblings("button");

    if (isSelectAll($elements) && $button.text() === SELECT_ALL) {
      $button.text(UNSELECT_ALL);
    } else if (!isSelectAll($elements) && $button.text() === UNSELECT_ALL) {
      $button.text(SELECT_ALL);
    }
  }

  function clickButtonHandler(event) {
    let $button = $(event.target);
    let $elements = $button.nextAll("li");

    if (isSelectAll($elements)) {
      unSelectAll($elements);
      $button.text(SELECT_ALL);
    } else {
      selectAll($elements);
      $button.text(UNSELECT_ALL);
    }

    return false;
  }

  function isSelectAll(elements) {
    let status = true;

    $(elements).each(function (_, element) {
      if (!$(element).find("label > input").prop("checked")) {
        status = false;
      }
    });
    return status;
  }

  function unSelectAll(elements) {
    $(elements).each(function (_, element) {
      $(element).find("label > input").prop("checked", false).trigger("change");
    });
  }

  function selectAll(elements) {
    $(elements).each(function (_, element) {
      $(element).find("label > input").prop("checked", true).trigger("change");
    });
  }

  $(document).ready(function () {
    addHandlerToFlagsFieldButton();
  });
})(django.jQuery);
