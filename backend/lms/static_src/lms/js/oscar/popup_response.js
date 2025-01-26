(function () {
  "use strict";
  var initData = JSON.parse(
    document.getElementById("lms-popup-response-constants").dataset
      .popupResponse,
  );
  switch (initData.action) {
    case "change":
      window.opener.lms.dismissChangeRelatedObjectPopup(
        window,
        initData.value,
        initData.obj,
        initData.new_value,
      );
      break;
    case "delete":
      window.opener.lms.dismissDeleteRelatedObjectPopup(window, initData.value);
      break;
    default:
      window.opener.lms.dismissAddRelatedObjectPopup(
        window,
        initData.value,
        initData.obj,
      );
      break;
  }
})();
