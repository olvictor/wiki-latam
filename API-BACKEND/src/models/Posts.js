const { DataTypes } = require('sequelize');
const sequelize = require('../config/db_connection');
const User = require('./Users');

const Post = sequelize.define(
  'Post',
  {
    id: {
      type: DataTypes.INTEGER,
      primaryKey:true,
      autoIncrement: true,
    },
    title: {
      type: DataTypes.STRING,
      allowNull:false,
      unique:true
    },
    content: {
      type: DataTypes.TEXT,
      allowNull:false,
      unique:true
    },
  },
  {
    timestamps: true,
  },
  {
  },
);

User.hasMany(Post, { foreignKey: "user_id" });
Post.belongsTo(User, { foreignKey: "user_id" });

module.exports = Post;