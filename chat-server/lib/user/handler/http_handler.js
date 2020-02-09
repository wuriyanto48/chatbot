class HttpHandler {
    constructor(){}

    index(req, res, next) {
        res.render('index');
    }
      
    chat(req, res, next) {
        //const user = req.user;
        res.render('chat', {'user': 'Aku'});
    }
}
  
module.exports = HttpHandler;