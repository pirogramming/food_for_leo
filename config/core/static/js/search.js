$(".hover").mouseleave(
    function () {
        $(this).removeClass("hover");
    }
);

function fetchJsonFilter(val) {
    var tags = [];
    //brand name filtering
    fetch('../../static/json/core_brand.json').then(function (response) {
        response.text().then(function (text) {
            var b_list = JSON.parse(text);
            var show_brand = [];
            b_list.filter(function (element, index, array) {
                if (array[index].name.includes(val)) {
                    console.log(array[index].name)
                    show_brand.push(array[index]);
                }
            });
            var brand_tag = '<li class="list-group-item">'  + show_brand[0].name + '</li>'
            tags = tags + brand_tag
        })
    })
    //product name filtering
    fetch('../../static/json/core_product.json').then(function (response) {
        response.text().then(function (text) {
            var p_list = JSON.parse(text);
            var show_product = [];
            p_list.filter(function (element, index, array) { //필터링하기
                if (array[index].name.includes(val)) {
                    console.log(array[index].name)
                    show_product.push(array[index]);
                }
            });
            for (var i = 0; i < show_product.length; i++) {
                if (i > 4) {
                    break
                } else {
                    var product = show_product[i];
                    var tag = "<li class=\"list-group-item\">"+"<a href=\"\">" +  product.name +'</a>' + '</li>'
                    tags = tags + tag
                }
            }
            document.querySelector('#result').innerHTML = tags;
        })
    })
}

$('.search').on('keyup', function () {
    var searchInput = $(this).val();
    if (searchInput.length <= 1) { //검색에 1개 이하일때 아무것도 안보여줌
        document.querySelector('#result').innerHTML = []
    } else {
        fetchJsonFilter(searchInput)
    }
});
