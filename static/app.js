function goBack() {
  window.history.back()
}



// to get species name when click on
$('.get-species').click(function(){

    species_id = $(this).siblings('.searchtesting').text()
    $('#allsearch-form').val(species_id)
    $("#search-form").submit()
})