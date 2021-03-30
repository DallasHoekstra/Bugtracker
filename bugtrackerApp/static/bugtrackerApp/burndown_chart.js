// getCookie Provided by Django in the Official Docs
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    $(".add-button").click(function() {
        var bug_id = $(".article-title")[0].text;
        // console.log(bug_id);

        // Making the AJAX Request
        $.ajax({
            url: window.location.href, 
            type: "POST",
            data: {
                bug_id: bug_id,
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                console.log("success");
                console.log(data); // Add button to the iteration side, recalculate stats
            },
            error: function (error) {
                console.log(error);
            }

        });
    });
});