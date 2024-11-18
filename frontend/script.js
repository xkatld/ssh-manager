document.getElementById('sshForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('name').value,
        host: document.getElementById('host').value,
        port: parseInt(document.getElementById('port').value),
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        category: document.getElementById('category').value
    };

    try {
        const response = await fetch('/ssh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        loadSSHList();
    } catch (error) {
        console.error('Error:', error);
    }
});

async function loadSSHList() {
    try {
        const response = await fetch('/ssh');
        const connections = await response.json();
        const list = document.getElementById('sshList');
        list.innerHTML = connections.map(conn => 
            `<div>
                ${conn.name} - ${conn.host}:${conn.port} (${conn.category})
             </div>`
        ).join('');
    } catch (error) {
        console.error('Error:', error);
    }
}

loadSSHList();
