var username = 'anonymous';
var host = 'ws://localhost:8000/';
var socket = new WebSocket(host);

socket.onopen = function() {
    console.log('connection opened...');

    socket.send(JSON.stringify({
        type: 'join', 
        data: {
            msg: 'halo', 
            date: new Date()
        }
    }));
}

socket.onerror = function(e) {
    console.log(e);
}

socket.onclose = function(e) {
    console.log(e);
}