$(document).ready(function () {
    // Every line of text will get written in exactly the value of total time (in ms)
    const totalTime = 4000;

    // array with texts to type in typewriter
    let dataText = [
        'The beginning is near. Let the angels protect you and the light guide you for what\'s to come 🌟',
        'Initiis Novis - New Beginnings | Spring 22',
        'Mystery evokes creativity. We’re all attracted to the answers we seek 🌸',
        'Not every story is perfect, that\'s the beauty of it 🌀'
    ];

    // type one text in the typewriter
    // keeps calling itself until the text is finished
    function typeWriter(text, i, fnCallback) {
        // check if text isn't finished yet
        if (i < (text.length)) {
            // add next character to h1
            document.querySelector("#typewriter").innerHTML = text.substring(0, i + 1) + '<span aria-hidden="true"></span>';

            // wait for a while and call this function again for next character
            setTimeout(function () {
                typeWriter(text, i + 1, fnCallback)
            }, totalTime / 60);
        }
        // text finished, call callback if there is a callback function
        else if (typeof fnCallback == 'function') {
            // call callback after timeout
            setTimeout(fnCallback, 3000);
        }
    }

    // start a typewriter animation for a text in the dataText array
    function StartTextAnimation(i) {
        if (i === dataText.length) {
            setTimeout(function () {
                StartTextAnimation(0);
            }, 3000);
        }
        // check if dataText[i] exists
        if (i < dataText.length) {
            // text exists! start typewriter animation
            typeWriter(dataText[i], 0, function () {
                // after callback (and whole text has been animated), start next text
                StartTextAnimation(i + 1);
            });
        }
    }

    // start the text animation
    StartTextAnimation(0);
})