const userInputField = $("#usernameInput");
const submitInput = $("#submitInput");
const errorOutput = $("#errorOutput");
const todoList = $('#todoList');
const listInput = $("#listInput");
const listAddButton = $("#listAddButton");
const addForm = $("#addForm");
const userForm = $("#userForm");

var loggedInUser = null;

function generateEscapedDivContent(str) {
    return $('<div></div>').text(str);
}

function generateListItem(itemText) {
    let htmlText = '<li class="textItem"></li>';
    let element = $(htmlText);
    element.text(itemText);
    element.on("click", handleRemove);
    return element;
}

// Helper function to do ajax requests -->
function ajaxPost(url, sendData, doneCallback) {
    $.ajax({
        method: "POST",
        url: url,
        data: sendData
    }).done(doneCallback);
}

var removeInProgress = false;
function handleRemove(e) {
    if(removeInProgress) {
        return;
    }

    removeInProgress = true;
    // TODO:
    // Use index to remove element from server side -->
    // e.parentNode
    let siblingIndices = $(e.target).parent().children();
    let index = -1;
    for(let i = 0; i < siblingIndices.length; i++) {
        if(siblingIndices[i] === e.target) {
            index = i;
            break;
        }
        // console.log(siblingIndices[i] === e.target);
    }

    if(index < 0) return;

    // console.log($.param({'index': index, 'user': loggedInUser}));
    ajaxPost("/remove", $.param({'index': index, 'user': loggedInUser}), (response) => {
        if(response.error) {
            console.log(response.error);
            return;
        }

        removeInProgress = false;
        loggedInUser.list = response['new_list'];

        renderList(response['new_list']);

    });


}

function handleAdd(e) {
    e.preventDefault();
    const rawUserData = listInput.val();
    if(rawUserData === "") {
        errorOutput.text("Invalid list add!");
        errorOutput.show();
    } else {
        errorOutput.hide();
        // console.log("DEBUG!");
        ajaxPost("/add", {'user': loggedInUser, 'item': rawUserData}, (response) => {
            // console.log(response);
            if(response.error) {
                console.log("Error: " + response.error);
                return;
            }
            loggedInUser.list = response.new_list;
            renderList(response.new_list);
        });
    }
}

function renderList(list) {
    todoList.html("");
    for(el in list) {
        let item = generateListItem(list[el]);
        item.on("click", handleRemove);
        todoList.append(item);
    }
}

function handleLogin(e) {
    // Prevent default form submission -->
    e.preventDefault();

    const rawUserData = userInputField.val();
    if(rawUserData.length === 0) {
        errorOutput.text("Invalid username!")
        errorOutput.show();
    } else {
        errorOutput.hide();
        ajaxPost("/login", {'username': rawUserData}, (response) => {
            // If error log it and return -->
            if(response.error) {
                console.log(response.error)
                return;
            }

            if(!loggedInUser) {
                // If no error and no logged user, render the list of items -->
                renderList(response.user.list);
                loggedInUser = response.user;
                addForm.show();
                userForm.hide();
            }
        });
    }
}

addForm.hide();
submitInput.on("click", handleLogin);
listAddButton.on("click", handleAdd);
