let fs = require('fs');
const User = require('../domain/user');

class UserRepository {
    constructor() {
    }

    async findByEmail(email) {
        return new Promise((resolve, reject) => {
            fs.readFile('users.json', 'utf8', (err, data) => {
                if(err){
                    reject(err);
                }
                const userData = JSON.parse(data);
                let user = '';
                for(let i=0;i<userData.length;i++){
                    if(email === userData[i].email){
                        user = userData[i];
                        break;
                    }
                }
                const userModel = new User(user.id, user.full_name, user.email, user.password);
                resolve(userModel);
            });
        });
    }
}

module.exports = UserRepository;