const User = require("./Users");
const Post = require("./Posts");

User.hasMany(Post, { foreignKey: "user_id" });
Post.belongsTo(User, { foreignKey: "user_id" });

module.exports = { User, Post };    