$("#left").click(function() {

    window.location = Number($("title")[0]["text"]) - 1;

});

$("#right").click(function() {

    window.location = Number($("title")[0]["text"]) + 1;

});


// $("#left_k").click(function() {
//
//     window.location = "keno/"+String(Number($("title")[0]["text"]) - 1);
//
// });
//
// $("#right_k").click(function() {
//
//     window.location = "keno/"+String(Number($("title")[0]["text"]) + 1);
//
// });