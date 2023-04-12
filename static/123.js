mydiv = document.getElementById("tt");
history2= document.getElementById("hh23");

function showhide(d,z) {
    d.style.display = "none";
    z.style.display = "block";
}
function showhideon(d,z) {
    d.style.display = "block";
    z.style.display = "none";
}
function search() {
    let input = document.getElementById("inputSearch");
    let filter = input.value.toUpperCase();
    let ul = document.getElementById("list");
    let li = ul.getElementsByTagName("li");
 
    
    for (let i = 0; i < li.length; i++) {
        let a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
document.addEventListener('keyup', search);