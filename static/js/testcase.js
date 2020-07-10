$("button[name='btn_delete_testcase']").click(function() {

    var data = { testcase_id : $(this).data('testcase_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_testcase",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_testcase']").click(function() {

    window.location = "edit_testcase?testcase_id="+$(this).data('testcase_id');

});




