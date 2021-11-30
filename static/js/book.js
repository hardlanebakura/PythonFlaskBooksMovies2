var bookauthor = document.getElementsByClassName("bookauthor")[0];
var link = bookauthor.getElementsByTagName("a")[0];
var authorname = link.getAttribute("href").substr(14);
console.log(authorname);
authorname = authorname.replaceAll(" ", "");
console.log(authorname);
link.setAttribute("href", "/author/" + authorname);