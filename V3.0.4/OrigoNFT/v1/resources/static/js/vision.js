window.addEventListener('load', function () {
    // A function to change the placement of the CODEX element
    function handleResize() {
        let codexElement = $('#vision-center-image-parent');
        let smallerParent = $('#smaller-parent-mark');
        let biggerParent = $('#bigger-parent-mark');

        if ($('body').width() < 769) {
            smallerParent.after(codexElement);
        } else {
            biggerParent.after(codexElement);
        }
    }

    handleResize();
    $(window).on("resize", handleResize);

    let scrollBtn = $("#scrollBtn");
    scrollBtn.click(() => {
        window.scroll({top: 0, left: 0, behavior: 'smooth'});
    })

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (document.body.scrollTop > window.innerHeight / 2 || document.documentElement.scrollTop > window.innerHeight / 2) {
            scrollBtn.show();
        } else {
            scrollBtn.hide();
        }
    }

});

