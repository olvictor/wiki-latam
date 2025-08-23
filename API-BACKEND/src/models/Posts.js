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
      validate: {
        notEmpty: {
          msg: "O campo title não pode estar vazio."
        },
        len: {
          args: [3, 255],
          msg: "O título deve ter entre 3 e 255 caracteres."
        }
      }
    },
    content: {
      type: DataTypes.TEXT,
      allowNull:false,
      validate: {
        notEmpty: {
          msg: "O campo content não pode estar vazio."
        }
      }
    }, 
    user_id: {               
      type: DataTypes.INTEGER,
      allowNull: false,
      validate: {
        notNull: {
          msg: "O campo user_id é obrigatório."
        }
      }
    },
  },
  {
    timestamps: true,
  },
  {
  },
);


module.exports = Post;