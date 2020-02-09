let passport = require('passport');
let LocalStrategy = require('passport-local').Strategy;

const passportConfig = {
    init: function(memberRepo){

        passport.serializeUser((user, done) => {
            done(null, user.email);
        });

        passport.deserializeUser(async (email, done) => {
            try{
                const result = await memberRepo.findByEmail(email);
                done(null, result);
            }catch(err){
                done(err);
            }
        });

        let strategy = new LocalStrategy({usernameField: 'email', passwordField: 'password', passReqToCallback: true}, async (req, username, password, done) => {
            try{
                const result = await memberRepo.findByEmail(username);
                if(!result){
                    done(null, false, req.flash('message', 'Username or password is not valid !!'));
                }else if(!result.isValidPassword(password)){
                    done(null, false, req.flash('message', 'Username or password is not valid !!'));
                }else{
                    done(null, result);
                }
            }catch(err){
                done(err);
            }
        });

        passport.use('local', strategy);
        return passport.initialize();
    },

    auth: function(){
        return passport.authenticate('local', {successRedirect: '/chat', failureRedirect: '/', failureFlash: true});
    },

    session: function(){
        return passport.session();
    }
};

module.exports = passportConfig;