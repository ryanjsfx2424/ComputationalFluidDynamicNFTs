const musicContainer = document.getElementById('music-container');
const playBtn = document.getElementById('play');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

const audio = document.getElementById('audio');

// Song titles
const songs = ['Origo song'];

// Keep track of song
let songIndex = 0;

// Initially load song details into DOM
loadSong(songs[songIndex]);

// Update song details
function loadSong(song) {
    audio.src = `./resources/static/music/${song}.wav`;
}

// Play song
function playSong() {
    musicContainer.classList.add('play');
    playBtn.querySelector('#music-stopped').classList.add('d-none');
    playBtn.querySelector('#music-playing').classList.remove('d-none')
    // playBtn.querySelector('i.fas').classList.remove('fa-play');
    // playBtn.querySelector('i.fas').classList.add('fa-pause');

    audio.play();
}

// Pause song
function pauseSong() {
    musicContainer.classList.remove('play');

    playBtn.querySelector('#music-stopped').classList.remove('d-none');
    playBtn.querySelector('#music-playing').classList.add('d-none')
    // playBtn.querySelector('i.fas').classList.add('fa-play');
    // playBtn.querySelector('i.fas').classList.remove('fa-pause');

    audio.pause();
}

// Previous song
function prevSong() {
    songIndex--;

    if (songIndex < 0) {
        songIndex = songs.length - 1;
    }

    loadSong(songs[songIndex]);

    playSong();
}

// Next song
function nextSong() {
    songIndex++;

    if (songIndex > songs.length - 1) {
        songIndex = 0;
    }

    loadSong(songs[songIndex]);

    playSong();
}


//get duration & currentTime for Time of song
function DurTime(e) {
    const {duration, currentTime} = e.srcElement;
    let sec;
    let sec_d;

    // define seconds currentTime
    function get_sec(x) {
        if (Math.floor(x) >= 60) {
            for (let i = 1; i <= 60; i++) {
                if (Math.floor(x) >= (60 * i) && Math.floor(x) < (60 * (i + 1))) {
                    sec = Math.floor(x) - (60 * i);
                    sec = sec < 10 ? '0' + sec : sec;
                }
            }
        } else {
            sec = Math.floor(x);
            sec = sec < 10 ? '0' + sec : sec;
        }
    }

    get_sec(currentTime, sec);

    function get_sec_d(x) {
        if (Math.floor(x) >= 60) {

            for (let i = 1; i <= 60; i++) {
                if (Math.floor(x) >= (60 * i) && Math.floor(x) < (60 * (i + 1))) {
                    sec_d = Math.floor(x) - (60 * i);
                    sec_d = sec_d < 10 ? '0' + sec_d : sec_d;
                }
            }
        } else {
            sec_d = (isNaN(duration) === true) ? '0' :
                Math.floor(x);
            sec_d = sec_d < 10 ? '0' + sec_d : sec_d;
        }
    }

    // define seconds duration

    get_sec_d(duration);

}

// Event listeners
playBtn.addEventListener('click', () => {
    const isPlaying = musicContainer.classList.contains('play');

    if (isPlaying) {
        pauseSong();
    } else {
        playSong();
    }
});

// Change song
prevBtn.addEventListener('click', prevSong);
nextBtn.addEventListener('click', nextSong);

// Song ends
audio.addEventListener('ended', nextSong);

// Time of song
audio.addEventListener('timeupdate', DurTime);