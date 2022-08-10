<!DOCTYPE html>
<html>
    <head>
        <title>Very Simple PHP gallery</title>
        <style>
            .fullscreen{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
            }  
            #gallery {
                z-index: 1;
            }
            .slide{   
                margin: 0 auto 0 auto;
                display: none;
                object-fit: contain;
                height: 100%;
                width: 100%;
            }  
            .showing{   
                display: block;
            }  
            #buttons {
                display: grid;
                z-index: 2;
                grid-template-columns: 10% 80% 10%;
                grid-template-areas: "left middle right";
            }
            .button {
                background-color: black;
                opacity: 20%;
                height: 100%;
                text-align: center;
                color: white;
                font-size: 3ch;
            }
            #button-left {
                /*grid-area: left;*/
                position: absolute;
                left: 0;
            }
            #button-right {
                /*grid-area: right;*/
                position: absolute;
                right: 0;
            }
        </style>
    </head>
    <body>
        <div id="gallery" class="fullscreen">
            <?php
            // (B) GET LIST OF IMAGE FILES FROM GALLERY FOLDER
            $dir = __DIR__ . DIRECTORY_SEPARATOR . "./" . DIRECTORY_SEPARATOR;
            $images = glob("$dir*.{jpg,jpeg,gif,png,bmp,webp}", GLOB_BRACE);

            // (C) OUTPUT IMAGES
            foreach ($images as $ind => $val) {
				if ($ind == 0) {
                    printf("<img class=\"slide showing\" src='%s'/>", basename($val));
                } else {
                    printf("<img class=\"slide\" src='%s'/>", basename($val));
                }
            }
            ?>
        </div>
        <div id="buttons" class="fullscreen">
            <button id="button-left" class="button" onclick="pauseSlideShow();nextSlide()"> << </button>
            <button id="button-right" class="button" onclick="pauseSlideShow();prevSlide()"> >> </button>
        </div>

        <script defer>
            function nextSlide(){  
                slides[currentSlide].className = 'slide';  
                currentSlide = (currentSlide+1)%slides.length;  
                slides[currentSlide].className = 'slide showing'; 
            }
            function prevSlide(){  
                slides[currentSlide].className = 'slide';  
                currentSlide = (currentSlide+(slides.length-1))%slides.length;  
                slides[currentSlide].className = 'slide showing'; 
            }
            // begin automatic slideshow
            function startSlideShow() {
                slideInterval = setInterval(nextSlide, 10000);  
            }
            // pause slideshow for 60 seconds
            function pauseSlideShow() {
                clearInterval(slideInterval);
                clearTimeout(slideTimeout);
                slideTimeout = setTimeout(startSlideShow, 60000);
            }

            var slides = document.querySelectorAll('.slide'); 
            var currentSlide = 0; 
            var slideInterval;  
            var slideTimeout;

            startSlideShow()
        </script>
    </body>
</html>
