function addComment(comment, post_id, user_name) {
    // document.body.scrollIntoView(false);
    fetch("/posts/add_comment", {
        method: "POST",
        body: JSON.stringify({comment:comment, post_id:post_id, user:user_name}),
    }).then((_res) => {
        location.reload();
    });
}