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
});
