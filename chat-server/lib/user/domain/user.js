const User = function(id, fullName, email, password){
    this.id = id;
    this.fullName = fullName;
    this.email = email;
    this.password = password;
}

User.prototype.isValidPassword = function(password){
    return this.password === password;
};

module.exports = User;