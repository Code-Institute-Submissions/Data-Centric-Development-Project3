function goBack() {
  window.history.back()
}



// to get species name when click on
$('.get-species').click(function(){

    // to identify when species column is clicked
    speciescolumn = $(this).attr("class")

    // if click on species column
    if (speciescolumn == 'species-onclick get-species'){
        // set species name
        species_name = $(this).text() 
        // parse selected species name into search form input
        $('#allsearch-form').val(species_name)
        // submit form
        $("#search-form").submit()

    }

    // else fetch the species name and submit
    else{
    // set species name
    species_name= $(this).siblings('.species-onclick').text() 
    // parse selected species name into search form input
    $('#allsearch-form').val(species_name)
    // submit form
    $("#search-form").submit()
    }
    

})