function login() {
    let username = document.querySelector('#username').value;
    let password = document.querySelector('#password').value;

    $.ajax({
        type: "POST",
        url: '/login',
        data: {
            json_string: JSON.stringify({username: username, password: password})
        },
        success: function (response) {
            if (response == "False") {
                window.alert("Incorrect username or password")
                window.location.href = '/login'
            }
            else {
                window.location.href = '/landing'
            }
        }
    })
}

function signup() {
    const username = document.querySelector("#username").value;
    const passsword = document.querySelector("#password").value;
    if (username == "" || passsword == "") {
        return "Failed";
    }
    $.ajax({
        type: "POST",
        url: '/signup',
        data: {
            json_string: JSON.stringify({username: username, password: passsword})
        },
        success: function (response) {
            if (response == "False") {
                window.alert("Username already taken");
                window.location.href = '/login';
                return "Failed"
            }
            else {
                window.location.href = '/landing'
            }
        }
    })
}

function logOut() {
    if (confirm("Are you sure you want to log out?")) {
        window.location.href = '/dropsession';
    }
}

function uploadImages() {
    document.querySelector('#upload').style.visibility = "visible";
}

function returnHome() {
    window.location.href = '/landing';
}

function myImages() {
    window.location.href = '/profile';
}

function fetchImagesforProfile() {
    $.ajax({
        type: "GET",
        url: '/user/images',
        success: function (response) {
            imagesDiv = document.querySelector("#images");
            for (let image of JSON.parse(response)) {
                let newImg = document.createElement("img");
                newImg.src = image["link"];
                newImg.onclick = function () {
                    if (confirm("delete this image?")) {
                        $.post(`delete/${image["name"]}`);
                        window.location.href = '/landing';
                    }
                }
                imagesDiv.appendChild(newImg);
            }
        }
    });
}

function fetchUserImages(user) {
    $.ajax({
        type: "GET",
        url: '/user/' + user + '/images',
        success: function (response) {
            imagesDiv = document.querySelector("#images");
            for (let image of JSON.parse(response)) {
                let newImg = document.createElement("img");
                newImg.src = image["link"];
                imagesDiv.appendChild(newImg);
            }
        }
    });
}

function fetchImagesforNewsfeed() {
    $.ajax({
       type: "GET",
       url: '/user/newsfeed',
       success: function (response) {
           imagesDiv = document.querySelector("#images");
           for (let image of JSON.parse(response)) {
               let newImg = document.createElement("img");
               newImg.src = image["link"];
               let newh2 = document.createElement("h2");
               node = document.createTextNode(image["user"]);
               newh2.appendChild(node);
               imagesDiv.appendChild(newh2);
               imagesDiv.appendChild(newImg);
           }
       }
    });
}

function searchUserName() {
    let targetUser = document.getElementById("searchUser").value;
    if (targetUser == "") return "Failed";
    $.ajax({
        type: "POST",
        url: '/search/' + targetUser,
        success: function (response) {
            if (response == "False") {
                window.alert("Username does not exist");
            }
            else if (response == "self") {
                window.location.href = '/profile';
            }
            else {
                window.location.href = '/search/' + targetUser;
            }
        }
    });
}

function followUser(user) {
    $.ajax({
                type: "POST",
                url: '/follow/' + user,
                success: function (response) {
                    window.location.href = '/search/' + user;
                }
    });
}

window.onload = () => {
    if (window.location.pathname == '/landing') {
        fetchImagesforNewsfeed();
    }
    if (window.location.pathname == '/profile') {
        fetchImagesforProfile();
    }
    path = window.location.pathname.split('/');
    if (path[1] == 'search') {
        fetchUserImages(path[2]);
    }
};
