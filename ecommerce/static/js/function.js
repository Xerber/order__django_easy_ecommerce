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
      
    
      console.log("data-index:", index);
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

    $('.product-quantity_cart').on('click', function () {
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

    $('.compare'). on('click', function(e){
        e.preventDefault();
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product id:", product_id);

        $.ajax({
          url: "/wishlist/add-to-wishlist",
          data: {
            'id': product_id
          },
          dataType: 'json',
          beforeSend: function(){
            console.log('Adding to wishlist..')
            this_val.html('✔')
          },
          success: function(response){
            console.log('Added to wishlist..')
          }
        })
    })

    $('a.product-remove_cart').on('click', function (e) {
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
          location.reload()
        }})
    })

    $('.product-remove-wishlist').on('click', function (e) {
      e.preventDefault();
      let wishlist_id = $(this).attr("data-wishlist-product")
      let this_val = $(this)

      console.log("wishlist_id", wishlist_id)
      console.log("current Element:", this_val)

      $.ajax ({
        url: '/wishlist/remove_from_wishlist',
        data: {
          'id': wishlist_id
        },
        dataType: 'json',
        beforeSend: function (){
          console.log('Deleting from wishlist')
        },
        success: function(response){
          console.log('Deleted from wishlist')
          $(".wishlist-list").html(response.data)
          location.reload()
        }
      })
    })

})

$(document).on("submit", "#contact-form-ajax", function(e){
  e.preventDefault()
  console.log('Отправляю')

  let firstname = $("#firstname").val()
  let lastname = $("#lastname").val()
  let email = $("#email").val()
  let phone = $("#phone").val()
  let subject = $("#subject").val()
  let message = $("#message").val()

  console.log("firstname", firstname);
  console.log("lastname", lastname);
  console.log("email", email);
  console.log("phone", phone);
  console.log("subject", subject);
  console.log("message", message);

  $.ajax({
    url: '/ajax-contact-form',
    data: {
      "firstname": firstname,
      "lastname": lastname,
      "email": email,
      "phone": phone,
      "subject": subject,
      "message": message,
    },
    dataType: "json",
    beforeSend: function(){
      console.log("Sending req to the server..")
    },
    success: function(response){
      console.log("Sent req to the server!")
      $("#contact-form-ajax").hide()
      $("#contact_as_p").hide()
      $("#message-response").html("Сообщение успешно отправлено")
    }
  })
})

$(document).on("submit", "#subscribe-form-ajax", function(e){
  e.preventDefault()
  console.log('Подписываю')

  let email = $("#email").val()
  console.log("email", email);

  $.ajax({
    url: '/ajax-subscribe-form',
    data: {
      "email": email,
    },
    dataType: "json",
    beforeSend: function(){
      console.log("Sending email to the server..")
    },
    success: function(response){
      console.log("Sent email to the server!")
      $("#subscribe_p").hide()
      console.log(response)
      if (response.data.bool == true) {
        $("#subscribe-form-ajax").hide()
        $("#message-response").html("Данный email успешно подписан!")
      }
      else {
        $("#message-response").html("Данный email уже подписан!")
      }
    }
  })
})