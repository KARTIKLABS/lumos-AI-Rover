const wsUrl = `ws://${window.location.host}/ws/telemetry`;
const ctrlUrl = `ws://${window.location.host}/ws/control`;

let telemetryWs, controlWs;

function connectWebSockets() {
    telemetryWs = new WebSocket(wsUrl);
    controlWs = new WebSocket(ctrlUrl);

    telemetryWs.onopen = () => {
        document.getElementById('conn-status').innerText = 'LINK ESTABLISHED';
        document.querySelector('.pulse').style.backgroundColor = 'var(--accent-green)';
    };

    telemetryWs.onclose = () => {
        document.getElementById('conn-status').innerText = 'CONNECTION LOST';
        document.querySelector('.pulse').style.backgroundColor = 'var(--accent-red)';
        setTimeout(connectWebSockets, 3000); // Auto reconnect
    };

    telemetryWs.onmessage = (event) => {
        const data = JSON.parse(event.data);
        document.getElementById('batt-val').innerText = data.battery.toFixed(1) + ' V';
        document.getElementById('temp-val').innerText = data.pi_temp.toFixed(1) + ' °C';
        document.getElementById('sonar-f-val').innerText = data.front_sonar + ' cm';
        document.getElementById('sonar-r-val').innerText = data.rear_sonar + ' cm';
    };
}

function sendCommand(dir) {
    if (controlWs && controlWs.readyState === WebSocket.OPEN) {
        controlWs.send(JSON.stringify({ action: 'drive', direction: dir }));
    }
}

// Event Listeners for controls
document.querySelectorAll('.btn-dir, .btn-stop').forEach(btn => {
    btn.addEventListener('mousedown', () => sendCommand(btn.dataset.dir));
    btn.addEventListener('mouseup', () => sendCommand('stop'));
    btn.addEventListener('mouseleave', () => sendCommand('stop'));
    
    // Touch support for mobile
    btn.addEventListener('touchstart', (e) => { e.preventDefault(); sendCommand(btn.dataset.dir); });
    btn.addEventListener('touchend', (e) => { e.preventDefault(); sendCommand('stop'); });
});

document.getElementById('btn-lock').addEventListener('click', () => {
    if (controlWs && controlWs.readyState === WebSocket.OPEN) {
        controlWs.send(JSON.stringify({ action: 'toggle_lock' }));
    }
});

document.getElementById('btn-estop').addEventListener('click', () => {
    if (controlWs && controlWs.readyState === WebSocket.OPEN) {
        controlWs.send(JSON.stringify({ action: 'estop' }));
    }
});

// Keyboard support (WASD)
window.addEventListener('keydown', (e) => {
    switch(e.key.toLowerCase()) {
        case 'w': sendCommand('forward'); break;
        case 's': sendCommand('backward'); break;
        case 'a': sendCommand('left'); break;
        case 'd': sendCommand('right'); break;
    }
});

window.addEventListener('keyup', (e) => {
    if (['w','a','s','d'].includes(e.key.toLowerCase())) {
        sendCommand('stop');
    }
});

connectWebSockets();
