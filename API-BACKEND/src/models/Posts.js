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
    },
    content: {
      type: DataTypes.TEXT,
      allowNull:false,
    }, 
    user_id: {               
      type: DataTypes.INTEGER,
      allowNull: false
    }
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