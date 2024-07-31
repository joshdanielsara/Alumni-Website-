document.addEventListener('DOMContentLoaded', () => {
    // Function to get CSRF token dynamically
    const getCsrfToken = () => {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    };

    // Handling comment form submission
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const postId = form.getAttribute('id').replace('commentForm', '');
            const commentInput = form.querySelector('.comment-input');
            const commentsContainer = document.getElementById(`commentsContainer${postId}`);
            const csrfToken = getCsrfToken();

            fetch(form.getAttribute('action'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({
                    'content': commentInput.value,
                }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(response => {
                commentsContainer.innerHTML += response;
                commentInput.value = '';
                location.reload();
            })
            .catch(error => {
                console.error('Error during fetch operation:', error);
            });
        });
    });

    // Handling like button clicks
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;
            const likeCountElement = button.previousElementSibling;

            fetch(`/like/${postId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    likeCountElement.textContent = data.likes;
                    button.classList.toggle('liked', data.liked);
                })
                .catch(error => {
                    console.error('Error during fetch operation:', error);
                });
        });
    });

    // Handling main comment submission
    const mainCommentButton = document.getElementById('main-comment-button');
    const mainCommentInput = document.getElementById('main-comment-input');

    const submitMainComment = () => {
        const commentsContainer = document.getElementById('comments');
        const csrfToken = getCsrfToken();
        const mainPostId = document.getElementById('seemore').dataset.postId;

        fetch(`/post_comment/${mainPostId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: new URLSearchParams({
                'content': mainCommentInput.value,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Expect JSON response with new comment data
        })
        .then(data => {
            // Create a new comment element based on the response data
            const commentElement = document.createElement('p');
            commentElement.classList.add('comment');
            commentElement.setAttribute('data-comment-id', data.comment.id);

            const userLink = document.createElement('a');
            userLink.href = `/profile/${data.comment.user.username}/`;
            userLink.textContent = data.comment.user.first_name;
            userLink.style.textDecoration = 'none';
            userLink.style.color = 'blue';

            const commentText = document.createTextNode(`: ${data.comment.content} | `);

            const commentDetails = document.createElement('span');
            commentDetails.classList.add('comment_details');
            commentDetails.textContent = data.comment.created_at;

            commentElement.appendChild(userLink);
            commentElement.appendChild(commentText);
            commentElement.appendChild(commentDetails);

            if (data.comment.user.username === '{{ request.user.username }}') {
                const deleteIcon = document.createElement('i');
                deleteIcon.classList.add('material-icons', 'delete-comment');
                deleteIcon.textContent = 'delete';
                deleteIcon.setAttribute('data-comment-id', data.comment.id);
                deleteIcon.style.cursor = 'pointer';
                commentElement.appendChild(deleteIcon);
            }

            commentsContainer.appendChild(commentElement);
            mainCommentInput.value = '';
            updateCommentCount(mainPostId);  // Increment the comment count
            updateMainComments(mainPostId); // Ensure comments are up to date

            // Optionally, set a flag for re-opening the 'seemore' section
            localStorage.setItem('openPostId', mainPostId);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
        });
    };

    if (mainCommentButton) {
        mainCommentButton.addEventListener('click', submitMainComment);
    }

    if (mainCommentInput) {
        mainCommentInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                submitMainComment();
            }
        });
    }

    // Handling main like button clicks
    const mainLikeButton = document.getElementById('main-like-button');
    if (mainLikeButton) {
        mainLikeButton.addEventListener('click', function () {
            const likeCountElement = document.getElementById('like-count');
            const mainPostId = document.getElementById('seemore').dataset.postId;

            fetch(`/like/${mainPostId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    likeCountElement.textContent = data.likes;
                    mainLikeButton.classList.toggle('liked', data.liked);
                })
                .catch(error => {
                    console.error('Error during fetch operation:', error);
                });
        });
    }

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-comment')) {
            const commentId = event.target.dataset.commentId;
            const commentElement = event.target.closest('.comment');
            const boxElement = commentElement.closest('.box');
            const postId = boxElement ? boxElement.dataset.postId : document.getElementById('seemore').dataset.postId;

            console.log('Comment ID:', commentId);
            console.log('Post ID:', postId);

            fetch(`/delete_comment/${commentId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    commentElement.remove();
                    updateCommentCount(postId, false);  // Decrement the comment count
                } else {
                    console.error('Error deleting comment:', data.error);
                }
            })
            .catch(error => {
                console.error('Error during fetch operation:', error);
            });
        }
    });

    // Function to update comment count
    function updateCommentCount(postId, increment = true) {
        const boxCommentCount = document.querySelector(`.box[data-post-id="${postId}"] .comment-count`);
        const mainCommentCount = document.getElementById('comment-count');

        if (boxCommentCount && mainCommentCount) {
            const newCount = increment ? parseInt(boxCommentCount.textContent) + 1 : parseInt(boxCommentCount.textContent) - 1;
            boxCommentCount.textContent = newCount;
            mainCommentCount.textContent = newCount;
        }
    }

    // Function to fetch and update comments for the main section without closing it
    function updateMainComments(postId) {
        fetch(`/get_comments/${postId}/`)
            .then(response => response.json())
            .then(data => {
                const commentsContainer = document.getElementById('comments');
                commentsContainer.innerHTML = '';

                data.comments.forEach(comment => {
                    const commentElement = document.createElement('p');
                    commentElement.classList.add('comment');
                    commentElement.setAttribute('data-comment-id', comment.id);

                    const userLink = document.createElement('a');
                    userLink.href = `/profile/${comment.user.username}/`;
                    userLink.textContent = comment.user.first_name;
                    userLink.style.textDecoration = 'none';
                    userLink.style.color = 'blue';

                    const commentText = document.createTextNode(`: ${comment.content} | `);

                    const commentDetails = document.createElement('span');
                    commentDetails.classList.add('comment_details');
                    commentDetails.textContent = comment.created_at;

                    commentElement.appendChild(userLink);
                    commentElement.appendChild(commentText);
                    commentElement.appendChild(commentDetails);

                    if (comment.user.username === '{{ request.user.username }}') {
                        const deleteIcon = document.createElement('i');
                        deleteIcon.classList.add('material-icons', 'delete-comment');
                        deleteIcon.textContent = 'delete';
                        deleteIcon.setAttribute('data-comment-id', comment.id);
                        deleteIcon.style.cursor = 'pointer';
                        commentElement.appendChild(deleteIcon);
                    }

                    commentsContainer.appendChild(commentElement);
                });
            })
            .catch(error => {
                console.error('Error fetching comments:', error);
            });
    }

    // Function to show more details
    function showMore(element) {
        const boxElement = element.closest('.box');
        const mainPostId = boxElement.getAttribute('data-post-id');
        const caption = boxElement.querySelector('.caption').textContent;
        const likesCount = boxElement.querySelector('.like-count').textContent.trim();
        const commentsCount = boxElement.querySelector('.comment-count').textContent.trim();
        const comments = boxElement.querySelectorAll('.comment');
        const photo = boxElement.querySelector('.post-photo');
        const video = boxElement.querySelector('.post-video');

        const mainImage = document.getElementById('main-image');
        const mainVideo = document.getElementById('main-video');
        const mainVideoSource = document.getElementById('main-video-source');
        const mainCaption = document.getElementById('main-caption');
        const likeCountElement = document.getElementById('like-count');
        const commentCountElement = document.getElementById('comment-count');
        const commentsContainer = document.getElementById('comments');

        const profileBaseUrlTemplate = document.querySelector('.container').getAttribute('data-profile-url');

        mainCaption.textContent = caption;
        likeCountElement.textContent = likesCount;
        commentCountElement.textContent = commentsCount;
        commentsContainer.innerHTML = '';

        comments.forEach(comment => {
            const username = comment.getAttribute('data-username');
            const firstname = comment.getAttribute('data-firstname');
            const createdat = comment.getAttribute('data-createdat');
            const profileUrl = profileBaseUrlTemplate.replace('USERNAME_PLACEHOLDER', username);
            const commentText = comment.textContent.split(': ')[1].split(' | ')[0];
            const commentId = comment.getAttribute('data-comment-id');
            const isUserComment = comment.querySelector('.delete-comment') !== null;

            commentsContainer.innerHTML += `<p class="comment" data-comment-id="${commentId}">
                <a href="${profileUrl}" style="text-decoration: none;color: blue;">${firstname}</a>
                : ${commentText} | <span class="comment_details">${createdat}</span>
                ${isUserComment ? `<i class="material-icons delete-comment" data-comment-id="${commentId}" style="cursor: pointer;">delete</i>` : ''}
            </p>`;
        });

        if (photo) {
            mainImage.src = photo.src;
            mainImage.style.display = 'block';
        } else {
            mainImage.style.display = 'none';
        }

        if (video) {
            mainVideoSource.src = video.querySelector('source').src;
            mainVideo.load();
            mainVideo.style.display = 'block';
        } else {
            mainVideo.style.display = 'none';
        }

        const seemoreElement = document.getElementById('seemore');
        const containerElement = document.getElementById('container');
        seemoreElement.style.display = 'block';
        containerElement.style.filter = 'blur(5px)';
        seemoreElement.setAttribute('data-post-id', mainPostId);

        // Store the post ID in local storage
        localStorage.setItem('openPostId', mainPostId);
    }

    function hideMore() {
        const seemoreElement = document.getElementById('seemore');
        const containerElement = document.getElementById('container');
        seemoreElement.style.display = 'none';
        containerElement.style.filter = 'none';
    }
});
