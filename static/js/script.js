$(document).ready(function () {

    function showStatus() {
        
        var $statusBar = $('#status');
        var icon = '';
        
        // Set status class, text, and open animation
        $('#status').children('p').html('Click on the <i class="fa fa-location-arrow" aria-hidden="true"></i> button to get your current location.');
        $('#status').slideToggle();
        $('#locateBtn').addClass('pulse');

        // Status bar close animation
        $('#status').children('.close').on('click', function() {
            $('#status').slideToggle();
        });
    } 

    /* window.onload = function() {
        // Suggest to share location with message and button animation
        setTimeout(function() {
            showStatus();
            $('#locateBtn').addClass('pulse');
        }, 1000);
    }; */

    window.addEventListener ? 
    window.addEventListener("load",showStatus(),false) : 
    window.attachEvent && window.attachEvent("onload",showStatus);
   
    
});