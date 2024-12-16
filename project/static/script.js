console.log("Script loaded");
const maindiv = document.getElementById('content');




function ErrorMessage(error){
    const div = document.getElementById('error-mes');
    div.textContent = error;
    div.style.display = 'block';
}




document.getElementById('save').addEventListener('click', function(){
    let text = maindiv.innerHTML;
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({ content: text })
    }).then(response => {
        if (response.ok) {
            ErrorMessage('Save successful!');
        } else {
            ErrorMessage('Error saving note.');
        }
    });
});
