var genres = document.getElementsByClassName("moviegenre");

for (let i = 0; i < genres.length; i++) {
    genres[i].innerHTML = genres[i].innerHTML.replace(",", "");
}

