$(document)
.ready(function () {

 $('.ui.search')
  .search({
      apiSettings: {
          url: 'search?q={query}'
      },
      type: 'category'
  });

  $('.ui.dropdown')
   .dropdown();

  $('input.prompt')
   .focus(function(evt) {
    $('section.content').fadeTo("fast", 0.2);
   })
   .focusout(function(evt){
    $('section.content').fadeTo("fast", 1);
    });

  $('body')
  // default everything
  .transition();

});
