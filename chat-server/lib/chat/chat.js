const WebSocket = require('ws');
const request = require('request');

const broadcastMessage = (listener, message) => {
    listener.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(message));
        }
    });
};

const sendPrivateMessage = (listener, message) => {
    listener.clients.forEach((client) => {

        if (client.readyState === WebSocket.OPEN) {

            if (client.room[message.data.to]){
                client.send(JSON.stringify(message));
            }
        }
    });
};

module.exports = (listener, userRepo) => {

    listener.on('connection', (socket, req) => {
        // create empty room
        socket.room = {};

        // console.log('----*****----');
        // console.log(req.session.passport.user);

        // // create room by user's email
        // socket.room[req.session.passport.user] = true;

        socket.on('message', async (message) => {
            const msg = JSON.parse(message);
            console.log(msg.type);

            switch(msg.type) {
                case 'join':
                    const data = await userRepo.findByEmail(msg.data);
                    request.post('http://localhost:9000/bot', {
                        json: {
                            sentence: 'halo'
                        }
                    }, (err, resp, body) => {
                        if (err) {
                            console.log(err);
                        }

                        socket.send(JSON.stringify({
                            type: 'chat_message', 
                            data: {
                                from: 'Bot',
                                msg: body.reply, 
                                date: new Date()
                            }
                        }));
                    });
                    break;
                case 'send_message':

                    socket.send(JSON.stringify({
                        type: 'chat_message', 
                        data: {
                            from: msg.data.from,
                            msg: msg.data.msg, 
                            date: new Date()
                        }
                    }));
                    
                    request.post('http://localhost:9000/bot', {
                        json: {
                            sentence: msg.data.msg
                        }
                    }, (err, resp, body) => {
                        if (err) {
                            console.log(err);
                        }

                        socket.send(JSON.stringify({
                            type: 'chat_message', 
                            data: {
                                from: 'Bot',
                                msg: body.reply, 
                                date: new Date()
                            }
                        }));
                    });

                    break;
                default:
                    console.log('unknown type');
            }
        });

        socket.on('close', (e) => {
            console.log('connection closed ', e);
        });

        socket.on('error', (e) => {
            console.log('connection error ', e);
        });

    });
};