function open_comments(clicked_id)
{
    let main_id = clicked_id.split(' ')[1];
    let open_button = document.getElementById('open '.concat(main_id)),
        close_button = document.getElementById('close '.concat(main_id)),
        window = document.getElementById("modal "+main_id);

    let class1 = "reply-comments_visible", class2 = "reply-comments_hidden";
    open_close_modal(open_button, close_button, window, class1, class2)
}

function open_close_modal(open_button, close_button, window, class1, class2){
    open_button.classList.remove(class1)
    open_button.classList.add(class2)

    close_button.classList.remove(class2)
    close_button.classList.add(class1)

    window.classList.remove(class2)
    window.classList.add(class1)
}

function close_comments(clicked_id)
{
    let main_id2 = clicked_id.split(' ')[1];
    let open_button = document.getElementById('open '.concat(main_id2)),
        close_button = document.getElementById('close '.concat(main_id2)),
        window = document.getElementById("modal "+main_id2);

    let class1 = "reply-comments_hidden", class2 = "reply-comments_visible";
    open_close_modal(open_button, close_button, window, class1, class2)
}
