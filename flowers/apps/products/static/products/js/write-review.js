function write_comment()
{
    let class1 = 'write-comment_visible', class2 = 'write-comment_hidden',
        button1 = 'open-write', button2 = 'close-write';

    open_close_comment(class1, class2, button1, button2)
}

function open_close_comment(class1, class2, button1, button2)
{
    let window = document.getElementById("modal-comment"),
        open_button = document.getElementById(button1),
        close_button = document.getElementById(button2);

    window.classList.remove(class2)
    window.classList.add(class1)
    open_button.classList.remove('write-comment_visible')
    open_button.classList.add('write-comment_hidden')
    close_button.classList.remove('write-comment_hidden')
    close_button.classList.add('write-comment_visible')
}

function close_write_comment()
{
    let class1 = 'write-comment_hidden', class2 = 'write-comment_visible',
        button1 = 'open-write', button2 = 'close-write';

    open_close_comment(class1, class2, button2, button1)
}