$(document).on('submit', '#search', (e) => {
    e.preventDefault()
    $.ajax({
        type: "POST",
        url: "usersearch"
    })
})

