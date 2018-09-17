(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle").click(function(e) {
    e.preventDefault();
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($window.width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    event.preventDefault();
  });






})(jQuery); // End of use strict
function CheckLogin(user)
{
  if(user=='AnonymousUser'){
      window.location.href = "/Auth/login/";
  }
}
function Load_Menu_Session(session)
{
  $.each(session, function(i, item) {

    if(item.fields.MenuParent==null)
    {
      var icon=item.fields.MenuIcon;
      var nm=item.fields.MenuName;
      var t=item.fields.MenuType;

      var liElement = document.createElement("li");
      var aElement = document.createElement("a");
      var spanElement = document.createElement("span");
      var iElement = document.createElement("i");
      iElement.setAttribute('class',icon);
      spanElement.innerText=nm;

      aElement.appendChild(iElement);
      aElement.appendChild(spanElement);
      liElement.appendChild(aElement);

      if(t=='MT01'){
        liElement.setAttribute('class','nav-item dropdown');
        aElement.setAttribute('class','nav-link dropdown-toggle');
        aElement.setAttribute('href','#');
        aElement.setAttribute('data-toggle','dropdown');

        var divElement=load_menu_init(session,item.pk);

        liElement.appendChild(divElement);
      }else{
        liElement.setAttribute('class','nav-item');
        aElement.setAttribute('class','nav-link');
        aElement.setAttribute('href',item.fields.MenuLink);
      }
      document.getElementById("Menu_Wrapper").appendChild(liElement);
    }
  });
}
function load_menu_init(session,ParentID){
  var divElement=document.createElement("div");;
  divElement.setAttribute('class','dropdown-menu');
  divElement.setAttribute('aria-labelledby','pagesDropdown');

  $.each(session, function(i, item) {
    var nm=item.fields.MenuName;
    var link=item.fields.MenuLink;
    var par=item.fields.MenuParent;

    if(par==ParentID)
    {
      var aElement = document.createElement("a");
      aElement.setAttribute('class','dropdown-item');
      aElement.setAttribute('href',link);
      aElement.innerText=nm;
      divElement.appendChild(aElement);
    }

  });
  return divElement;
}
