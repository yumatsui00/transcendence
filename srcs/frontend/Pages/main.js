function fetchData() {
    fetch('/api/')
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerText = JSON.stringify(data);
        })
        .catch(error => console.error('Error:', error));
}
