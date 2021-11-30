popularwriters = document.getElementsByClassName("popularwriters")[0];
popularlinks = popularwriters.getElementsByTagName("a");
console.log(popularlinks.length);
for (let i = 0; i < popularlinks.length; i++) {

authorname = popularlinks[i].getAttribute("href").substr(14);
authorname = authorname.replaceAll(" ", "");
console.log(authorname);
popularlinks[i].setAttribute("href", "/author/" + authorname);

}