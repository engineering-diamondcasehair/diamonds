var setVideoHeight = function() {
    setInterval(function() {
        var biggestHeight = 0;
        // Loop through elements children to find & set the biggest height
        $("#homepage-atf-wrapper *").each(function() {
            // If this elements height is bigger than the biggestHeight
            if ($(this).height() > biggestHeight) {
                // Set the biggestHeight to this Height
                biggestHeight = $(this).height();
            }
            if (biggestHeight < $('#homepage-video-text').height()) {
                biggestHeight = $('#homepage-video-text').height();
            }
        })

        // Set the container height
        $("#homepage-video-wrapper").height(biggestHeight);
        $("#homepage-video-text").height(biggestHeight);
    });
}