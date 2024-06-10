    // Get all mini images
    var miniImages = document.querySelectorAll(".mini-image");
    var fullscreenImgContainer = document.querySelector(".fullscreen-img");
    var fullscreenImg = document.getElementById("fullscreen-image");
    var prueba = document.getElementById("ofw3gkjet5nt");
    // Click event on mini image
    miniImages.forEach(function (miniImage) {
        miniImage.addEventListener("click", function () {
            // Show image in full screen
            fullscreenImg.src = this.src;
            fullscreenImgContainer.style.display = "flex";
        });
    });

    // Hide image in full screen when clicking on it
    fullscreenImgContainer.addEventListener("click", function () {
        this.style.display = "none";
    });
