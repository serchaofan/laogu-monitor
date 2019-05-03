$(document).ready(function () {
    $('#list').DataTable({
        language: {
            url: "/static/datatable_chinese.json"
        }
    });

    // $("input[type='checkbox']").iCheck({
    //     checkboxClass: 'icheckbox_square-blue',
    //     radioClass: 'iradio_square-blue',
    // });
});

// $('#select_all').on('ifChecked', function(event) {
//     $('input').iCheck('check');
// });
// $('#select_all').on('ifUnchecked', function(event) {
//     $('input').iCheck('uncheck');
// });
//
function swapCheck() {

    var checkAll = $("input#select_all");  //全选的input
    var checkboxs = $("input#test"); //所有单选的input

    checkAll.on('ifChecked ifUnchecked', function (event) {
        if (event.type == 'ifChecked') {
            checkboxs.iCheck('check');
        } else {
            checkboxs.iCheck('uncheck');
        }
    });

    checkboxs.on('ifChanged', function (event) {
        if (checkboxs.filter(':checked').length == checkboxs.length) {
            checkAll.prop('checked', true);
        } else {
            // checkAll.removeProp('checked');
            checkAll.prop('checked', false);
        }
        checkAll.iCheck('update');
    })
}
//
// var isCheckAll = false;
//
// function swapCheck() {
//     if (isCheckAll) {
//         $("input[type='checkbox']").each(function () {
//             this.checked = false;
//         });
//         isCheckAll = false;
//     } else {
//         $("input[type='checkbox']").each(function () {
//             this.checked = true;
//         });
//         isCheckAll = true;
//     }
// }


var checkBoxArr = [];
$('input[id="test"]:checked').each(function() {
	checkBoxArr.push($(this).val());
	alert(checkBoxArr)
});
