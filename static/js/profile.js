function toggleEditMode() {
    var editMode = document.getElementById('editMode');
    var displayMode = document.getElementById('displayMode');
    var updateProfileBtn = document.getElementById('updateProfileBtn');

    if (editMode.style.display === 'none' || editMode.style.display === '') {
        // Switch to edit mode
        editMode.style.display = 'block';
        displayMode.style.display = 'none';
        updateProfileBtn.style.display = 'block';
    } else {
        // Switch to display mode
        editMode.style.display = 'none';
        displayMode.style.display = 'block';
        updateProfileBtn.style.display = 'none';
    }
}


document.addEventListener('DOMContentLoaded', function() {
    function toggleEditMode() {
        const editButton = document.getElementById('editButton');
        const editMode = document.getElementById('editMode');
        const displayMode = document.getElementById('displayMode');

        editButton.classList.toggle('hidden');
        editMode.classList.toggle('hidden');
        displayMode.classList.toggle('hidden');
    }

    const editButton = document.getElementById('editButton');
    if (editButton) {
        editButton.addEventListener('click', function() {
            toggleEditMode();
        });
    }

    const fieldsToEdit = ['first_name', 'middle_name', 'last_name', 'year_graduated', 'strand'];
    fieldsToEdit.forEach(function(fieldId) {
        const displayElement = document.getElementById(`display_${fieldId}`);
        if (displayElement) {
            displayElement.addEventListener('dblclick', function() {
                toggleEditMode();
            });
        }
    });
});







document.addEventListener("DOMContentLoaded", function() {
    const limitText = (selector, limit) => {
        document.querySelectorAll(selector).forEach(el => {
            el.querySelectorAll('p').forEach(p => {
                if (p.textContent.length > limit) {
                    p.textContent = p.textContent.substring(0, limit) + '...';
                }
            });
        });
    };

    limitText('#displayMode', 40);  // Adjust the limit as needed
});

