$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){

    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax(
        {
            type:"GET",
            url:"pluscart",
            data:{
                prod_id:id
            },
            success:function(data)
            {
                eml.innerText = data.quant
                document.getElementById("amt").innerText = data.amount
                document.getElementById("tax").innerText = data.tax
                document.getElementById("total").innerText = data.total
            }
        }
    )

})

$('.minus-cart').click(function(){

    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax(
        {
            type:"GET",
            url:"minuscart",
            data:{
                prod_id:id
            },
            success:function(data)
            {
                eml.innerText = data.quant
                document.getElementById("amt").innerText = data.amount
                document.getElementById("tax").innerText = data.tax
                document.getElementById("total").innerText = data.total
            }
        }
    )

})

$('.remove-item').click(function(){

    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax(
        {
            type:"GET",
            url:"removeitem",
            data:{
                prod_id:id
            },
            success:function(data)
            {
                eml.parentNode.parentNode.parentNode.parentNode.remove()
            }
        }
    )

})

// let elem = document.getElementById('faddtocart');


function clicked()
{
    let elem = document.getElementById("adding");
    elem.innerHTML = "ADDED";
    document.getElementById("elem").disabled = true;
}