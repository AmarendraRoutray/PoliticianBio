$(".sidebar-dropdown > a").click(function() {
    $(".sidebar-submenu").slideUp(200);
    if ( $(this).parent().hasClass("active")) {
      console.log($(this).parent().hasClass("active"));
      $(".sidebar-dropdown").removeClass("active");
      $(this).parent().removeClass("active");
        
    } else {
      $(".sidebar-dropdown").removeClass("active");
      $('.sidebar-sub-dropdown').slideDown(200);
      $(this).next(".sidebar-submenu").slideDown(200);
      $('.sidebar-sub-dropdown').slideDown(200);
      $(this).parent().addClass("active");
    }
  });
//sub-dropwown

$(".sidebar-sub-dropdown > a").click(function() {
  $(".sidebar-sub-submenu").slideUp(200);
  if (
    $(this)
      .parent()
      .hasClass("active")
  ) {
    $(".sidebar-sub-dropdown").removeClass("active");
    $(this)
      .parent()
      .removeClass("active");
  } else {
    $(".sidebar-sub-dropdown").removeClass("active");
    $(this)
      .next(".sidebar-sub-submenu")
      .slideDown(200);
    $(this)
      .parent()
      .addClass("active");
  }
});

$(".sidebar-sub2-dropdown > a").click(function() {
  $(".sidebar-sub2-submenu").slideUp(200);
  if (
    $(this)
      .parent()
      .hasClass("active")
  ) {
    $(".sidebar-sub2-dropdown").removeClass("active");
    $(this)
      .parent()
      .removeClass("active");
  } else {
    $(".sidebar-sub2-dropdown").removeClass("active");
    $(this)
      .next(".sidebar-sub2-submenu")
      .slideDown(200);
    $(this)
      .parent()
      .addClass("active");
  }
});

  // subdropdown
 

  $("#close-sidebar").click(function() {
    if ($(window).width() <= 425) {
      $('.sidebar-wrapper').css("display","none")
     }
     else {
      $(".page-wrapper").removeClass("toggled");
     }
  });

  $("#show-sidebar").click(function() {
    if ($(window).width() <= 425) {
      $('.sidebar-wrapper').css("display","block")
    }
    else {
      $(".page-wrapper").addClass("toggled");
    }
  });
  
  