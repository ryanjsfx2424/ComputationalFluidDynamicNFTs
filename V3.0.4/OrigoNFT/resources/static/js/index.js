$(document).ready(function () {
    $.fn.isOnScreen = function (test) {
        var height = this.outerHeight();
        var width = this.outerWidth();

        if (!width || !height) {
            return false;
        }

        if(width < 1200) {
            document.getElementById("p1p1").innerHTML = "Inspired by the people before and";
            document.getElementById("p1p2").innerHTML = "among us, we want to add beauty,";
            document.getElementById("p1p3").innerHTML = "hope, and passion to the web3 space.";
            document.getElementById("p1p4").innerHTML = "Origo is a collection of 3,000 1/1 hand";
            document.getElementById("p1p5").innerHTML = "-curated NFT's available by minting";
            document.getElementById("p1p6").innerHTML = "our access pass. Each Origo NFT is";
            document.getElementById("p1p7").innerHTML = "Unreal Engine ready, has exclusive";
            document.getElementById("p1p8").innerHTML = "access to undisclosed future utility,";
            document.getElementById("p1p9").innerHTML = "upcoming drops, projects and more.";

            document.getElementById("p2p1").innerHTML = "The key to Origo is through our Access Pass.";
            document.getElementById("p2p2").innerHTML = "One pass = one character from the 3,000";
            document.getElementById("p2p3").innerHTML = "character collection. Each member with a";
            document.getElementById("p2p4").innerHTML = "whitelist will be eligible to mint one pass";
            document.getElementById("p2p5").innerHTML = "which can later be exchanged for one of";
            document.getElementById("p2p6").innerHTML = "our character NFTs. There will be 3,000 passes";
            document.getElementById("p2p7").innerHTML = "equivalent to the number of characters, these";
            document.getElementById("p2p8").innerHTML = "will hold the unknown identity of your Origo.";
            document.getElementById("p2p9").innerHTML = "You may notice that some passes look unique";
            document.getElementById("p2p10").innerHTML = "in comparison to others. If this is the case, your";
            document.getElementById("p2p11").innerHTML = "pass may hold a more complex Origo identity";
            document.getElementById("p2p12").innerHTML = "which could result in more advanced metadata";
            document.getElementById("p2p13").innerHTML = "upon the reveal of your character.";
        }

        var win = $(window);

        var viewport = {
            top: win.scrollTop(),
            left: win.scrollLeft()
        };
        viewport.right = viewport.left + win.width();
        viewport.bottom = viewport.top + win.height();

        var bounds = this.offset();
        bounds.right = bounds.left + width;
        bounds.bottom = bounds.top + height;

        var deltas = {
            top: viewport.bottom - bounds.top,
            left: viewport.right - bounds.left,
            bottom: bounds.bottom - viewport.top,
            right: bounds.right - viewport.left
        };

        if (typeof test == 'function') {
            return test.call(this, deltas);
        }


        return deltas.top > 0
            && deltas.left > 0
            && deltas.right > 0
            && deltas.bottom > 0;
    };

    // Change background of navbar on mobile viewports when clicking navbar sandwich button
    $('#sandwich-button').click(() => {
        let navbar = $('#navbar');
        let navBgColor = navbar.css('background-color');
        if (navBgColor === 'rgba(0, 0, 0, 0)') {
            navbar.css('background-color', 'rgba(0, 0, 0, 0.8)');
        } else {
            navbar.css('background-color', 'rgba(0, 0, 0, 0)');
        }
    });

    let scrollBtn = $("#scrollBtn");
    let exploreList = $('#explore-list');
    let musicBtn = $('#music-container');

    // Get explore sections nav buttons
    let tabs = document.querySelectorAll('.eye');

    scrollBtn.click(() => {
        document.querySelector('.video-container').scrollIntoView({behavior: 'smooth'});
    })

    $('#explore-content').scroll(function () {
        scrollFunction();
    });

    function scrollFunction() {

        // When the user scrolls half the viewport height show the scroll to top button
        if ($('.video-container').isOnScreen(function (deltas) {
            return deltas.top >= 10 && deltas.bottom >= 10;
        })) {
            scrollBtn.fadeOut();
            exploreList.fadeOut();
            musicBtn.fadeIn();
        } else {
            scrollBtn.fadeIn();
            exploreList.fadeIn();
            musicBtn.fadeOut();
        }

        if ($('#explore-content-1').isOnScreen(function (deltas) {
            return deltas.top >= 10 && deltas.bottom >= 10;
        })) {
            tabs[0].classList.add('eye-active');
        } else {
            tabs[0].classList.remove('eye-active');
        }
        if ($('#explore-content-2').isOnScreen(function (deltas) {
            return deltas.top >= 10 && deltas.bottom >= 10;
        })) {
            tabs[1].classList.add('eye-active');
        } else {
            tabs[1].classList.remove('eye-active');
        }
        if ($('#explore-content-3').isOnScreen(function (deltas) {
            return deltas.top >= 10 && deltas.bottom >= 10;
        })) {
            tabs[2].classList.add('eye-active');
        } else {
            tabs[2].classList.remove('eye-active');
        }
        // if ($('#explore-content-4').isOnScreen(function (deltas) {
        //     return deltas.top >= 10 && deltas.bottom >= 10;
        // })) {
        //     tabs[3].classList.add('eye-active');
        // } else {
        //     tabs[3].classList.remove('eye-active');
        // }
        // if ($('#explore-content-5').isOnScreen(function (deltas) {
        //     return deltas.top >= 10 && deltas.bottom >= 10;
        // })) {
        //     tabs[4].classList.add('eye-active');
        // } else {
        //     tabs[4].classList.remove('eye-active');
        // }
    }

    // Define a place to scroll to for all the bottom nav items on the first section
    let categoriesElements = $('[data-scroll-to]');
    for (let el of categoriesElements) {
        $(el).click(() => {
            let scrollTo = document.querySelector($(el).attr('data-scroll-to'));
            scrollTo.scrollIntoView({behavior: 'smooth'});
        })
    }

    tabs.forEach(function (button) {
        button.addEventListener('click', function () {

            let scrollToEl = this.dataset.contentToShow;

            document.querySelector(scrollToEl).scrollIntoView({behavior: 'smooth'});

            toggleClass(tabs, this);
        });
    });

    function toggleClass(tabs, tabToActivate) {
        tabs.forEach(function (tab) {
            tab.classList.remove('eye-active');
            tab.classList.add('closed-eye');
        });


        if (tabToActivate.classList.contains('closed-eye'))
            tabToActivate.classList.remove('closed-eye')
        tabToActivate.classList.add('eye-active');

        //  Show the content this button is supposed to
        document.querySelector(tabToActivate.dataset.contentToShow).classList.remove('d-none');
    }
});