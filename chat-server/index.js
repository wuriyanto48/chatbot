const express = require('express');
const Websocket = require('ws');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
//require for passport
require('connect-ensure-login');
const session = require('express-session');
const flash = require('connect-flash');

const path = require('path');
const app = express();
const server = require('http').createServer(app);

const sessionParser = session({saveUninitialized: false, secret: 'wuryschat', resave: false});

const listener = new Websocket.Server({
    server: server,
    // verifyClient: function(info, done) {
    //     console.log('Parsing session from request...');
    //     sessionParser(info.req, {}, () => {
    //       console.log('Session is parsed!');
    
    //       //
    //       // We can reject the connection by returning false to done(). For example,
    //       // reject here if user is unknown.
    //       //
    //       done(info.req.session.passport);
    //     });
    //   }
});

// load env
require('dotenv').config();

const HttpHandler = require('./lib/user/handler/http_handler');
const UserRepo = require('./lib/user/repository/user_repo');
const httpHandler = new HttpHandler();
const userRepo = new UserRepo();

// init chat
require('./lib/chat/chat')(listener, userRepo);
const passport = require('./config/passport');

// set default PORT
const PORT = process.env.PORT;


//passport
app.use(sessionParser);
app.use(passport.init(userRepo));
app.use(passport.session());
app.use(flash());

//view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

//middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// routes
app.get('/', httpHandler.index);
app.post('/login', passport.auth());
app.get('/chat', httpHandler.chat);

// listen app on PORT
server.listen(PORT, err => {
    if (err) {
        console.log(`error on start up: ${err}`);
    } else {
        console.log(`app listen on port ${PORT}`);
    }
});
