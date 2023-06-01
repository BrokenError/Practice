function open_comments(clicked_id)
{
    let main_id = clicked_id.split(' ')[1];

    let class1 = "reply-comments_visible",
        class2 = "reply-comments_hidden";

    open_close_modal('open-comments ' + main_id, 'close-comments ' + main_id, class1, class2, main_id);
}

function open_close_modal(butt1, butt2, class1, class2, main_id)
{
    let open_button = document.getElementById(butt1),
        close_button = document.getElementById(butt2),
        window = document.getElementById("window-comments "+ main_id);

    open_button.classList.remove(class1)
    open_button.classList.add(class2)

    close_button.classList.remove(class2)
    close_button.classList.add(class1)

    window.classList.remove(class2)
    window.classList.add(class1)
}

function close_comments(clicked_id)
{
    let main_id = clicked_id.split(' ')[1];

    let class1 = "reply-comments_visible",
        class2 = "reply-comments_hidden";

    open_close_modal('open-comments ' + main_id, 'close-comments ' + main_id, class2, class1, main_id);
}
