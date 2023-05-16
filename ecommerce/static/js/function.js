$(document).ready(function(){
    $('.add-to-cart-btn').on('click', function (e) {
      e.preventDefault();
      let this_val = $(this)
      let index = this_val.attr("data-index")
    
      let quantity = $("#product-qty-" + index).val()
      let product_title = $("#product-title-" + index).val()
      let product_id = $("#product-id-" + index).val()
      let product_price = $("#product-price-" + index).text()
      let product_image = $("#product-image-" + index).val()
      let get_absolute_url = $("#product-get_absolute_url-" + index).attr("href")
      let to_url = $("#to_url").val()
      
    
      console.log("quantity:", quantity);
      console.log("product_title:", product_title);
      console.log("product_id:", product_id);
      console.log("product_price:", product_price);
      console.log("product_image:", product_image);
      console.log("get_absolute_url:", get_absolute_url);
      console.log("to_url:", to_url);
      console.log("current Element:", this_val);
    
      $.ajax ({
        url: to_url,
        data: {
          'id': product_id,
          'qty': quantity,
          'title': product_title,
          'price': product_price,
          'image': product_image,
          'get_absolute_url': get_absolute_url,
        },
        dataType: 'json',
        beforeSend: function(){
          console.log("Adding product to Cart..");
        },
        success: function(response){
          this_val.html("✔");
          console.log("Added product to Cart..");
          $(".cart-items-count").text(response.totalcartitems)
        }
      })
    
    })

    $('.product-remove_cl').on('click', function (e) {
    e.preventDefault();
    let product_id = $(this).attr("id")
    let this_val = $(this)

    console.log("product_id:", product_id);
    console.log("current Element:", this_val);

    $.ajax ({
      url: '/cart/delete-from-cart',
      data: {
        'id': product_id
      },
      dataType: 'json',
      beforeSend: function(){
        this_val.hide()
      },
      success: function(response){
        this_val.show()
        $(".cart-items-count").text(response.totalcartitems)
        $("#cart-list").html(response.data)
        location.reload();
      }})
    })

    $('.product-quantity_cl').on('click', function () {
      let quantity = $(this).val()
      let product_id = $(this).attr("id")
      let this_val = $(this)

      console.log("quantity:", quantity);
      console.log("product_id:", product_id);
      console.log("current Element:", this_val);

      $.ajax ({
        url: '/cart/update-quantity',
        data: {
          'id': product_id,
          'quantity': quantity
        },
        dataType: 'json',
        beforeSend: function(){
          console.log("Changing quantity..");
        },
        success: function(response){
          console.log("Changed quantity..");
          $(".cart-items-count").text(response.totalcartitems)
          $("#cart-list").html(response.data)
          location.reload();
        }
      })
    })

})