// Modal functions
function openEditModal() {
    document.getElementById('editModal').style = "overflow-y:scroll;"
    document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

function openResumeModal() {
    document.getElementById('resumeModal').style.display = 'block';
}

function closeResumeModal() {
    document.getElementById('resumeModal').style.display = 'none';
}

function viewResume(filename) {
    window.open(`${filename}`, '_blank');
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        event.target.style.display = 'none';
    }
}