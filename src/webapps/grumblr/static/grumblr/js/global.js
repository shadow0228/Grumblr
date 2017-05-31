var req;
var req2;

// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/get-post", true);
    req.send(); 
}

function sendRequest2() {
    if (window.XMLHttpRequest) {
        req2 = new XMLHttpRequest();
    } else {
        req2 = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req2.onreadystatechange = handleCommentResponse;
    req2.open("GET", "/get-comment", true);
    req2.send(); 
}


// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

function addComment(arg) {
    var text = document.getElementById("textfield" + arg).value;
    var post = document.getElementById("postId" + arg).value;

    var data = {'text':text, 'post':post}

    $.post("/add-comment/", data, function(response){
        
    });
}

function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items
    var list = document.getElementById("post");
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }

    // Parses the response to get a list of JavaScript objects for 
    // the items.
    var posts = JSON.parse(req.responseText);


    // Adds each new todo-list item to the list
    for (var i = 0; i < posts.length; ++i) {
        // Extracts the item id and text from the response
        var image = posts[i]["image"];
        var postText = posts[i]["postText"];
        var create = posts[i]["create"]
        var userId = posts[i]["userId"]
        var user = posts[i]['user']
        var postId = posts[i]["postId"]
        // var csrftoken = getCookie('csrftoken');

        // Builds a new HTML list item for the todo-list item
        var newPost = document.createElement("li");
        var newHTML = (
         '<div class="blog-post"; style="background-color:#F7F9F9; overflow: auto;">' +
            '<div>' +
              '<img src="' + image + '" width="10%" height="10%">' +
              '<p class="blog-post-meta"  style="float:right;">' +
              create +
              '<a href="/Profile/' + userId + '">' + user + '</a>' +
            '</div>' +
            '<div>' +
              '<br>' +
              '<p style="float:;">' + postText + '</p>' +
              '<br>' +
            '</div>' +
            '<input type="hidden" id="postId'+postId +'" value='+ postId +'>' +
              '<input type="text" id="textfield'+ postId +'">' +
              '<button id="addBtn" onclick="addComment(' + postId + ')">Post</button>' +
              '<br>' +
              '<br>' +
              '<br>' +
           '<ol id="comment'+ i +'">' +
            '</div>' 

          )

        newPost.innerHTML = newHTML
       
        // Adds the todo-list item to the HTML list
        list.appendChild(newPost);
    }
}




function handleCommentResponse() {

    if (req2.readyState != 4 || req2.status != 200) {
        return;
    }


    // Parses the response to get a list of JavaScript objects for 
    // the items.
    var comments = JSON.parse(req2.responseText);


    // Adds each new todo-list item to the list
    for (var i = 0; i < comments.length; ++i) {

         var list = document.getElementById("comment" + i);
         while (list.hasChildNodes()) {
                list.removeChild(list.firstChild);
            }

        for (var a = 0; a < comments[i].length; ++a) {


            var image = comments[i][a]["image"];
            var commentText = comments[i][a]["commentText"];
            var create = comments[i][a]["create"]
            var userId = comments[i][a]["userId"]
            var user = comments[i][a]['user']

            // Builds a new HTML list item for the todo-list item
            var newPost = document.createElement("li");
            var newHTML = (
            '<div class="blog-post"; style="background-color:#F7F9F9; overflow: auto;">' +
              '<img src="' + image + '" width="5%" height="5%">' +
              '<p class="blog-post-meta"  style="float:right;">' +
              create +
               '<a href="/Profile/' + userId + '">' + user + '</a>' +
              '<p class="blog-post-meta"</>' +
                commentText +
              '</p>' +
              '</div>'
                )

            newPost.innerHTML = newHTML
           
            // Adds the todo-list item to the HTML list
            list.appendChild(newPost);

        }
    }
}

window.setInterval(sendRequest, 5000);
window.setInterval(sendRequest2, 5000);

// causes the sendRequest function to run every 10 seconds

