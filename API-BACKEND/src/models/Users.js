const { DataTypes } = require('sequelize');
const sequelize = require('../config/db_connection');
const Role = require('../models/Roles');
const Post = require('./Posts');

const User = sequelize.define(
  'User',
  {
    id: {
      type: DataTypes.INTEGER,
      primaryKey:true,
      autoIncrement: true,
    },
    username: {
      type: DataTypes.STRING,
      allowNull:false,
      unique: {
        msg: "Este nome de usuário já está em uso."
      },
      validate: {
        notEmpty: {
          msg: "O campo username não pode estar vazio."
        },
        notNull: {
          msg: "O campo username é obrigatório."
        },
        len: {
          args: [3, 50],
          msg: "O nome de usuário deve ter entre 3 e 50 caracteres."
        }
      }
    },
    descricao: {
      type: DataTypes.STRING,
      allowNull:true,
    },
    password_hash:{
      type: DataTypes.STRING,
      allowNull:false,
      validate: {
        notEmpty: {
          msg: "O campo password não pode estar vazio."
        },
      }
    },
    email:{
      type: DataTypes.STRING,
      unique: {
        msg: "Este email já está em uso."
      },
      allowNull:false,
      validate: {
        notEmpty: {
          msg: "O campo email não pode estar vazio."
        },
        notNull: {
          msg: "O campo email é obrigatório."
        },
        isEmail: {
          msg: "O email fornecido não é válido."
        }
      }
    },
    role_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      validate: {
        notNull: {
          msg: "O campo role_id é obrigatório."
        }
      },
      onDelete: "CASCADE",
      onUpdate: "CASCADE"
    },
    img_url: {
      type: DataTypes.STRING,
      allowNull:false,
      defaultValue: "https://eaavatarservice.akamaized.net/production/avatar/prod/1/599/416x416.JPEG"
    },
    rede_twitter: {               
      type: DataTypes.STRING,
    },
    rede_instagram: {               
      type: DataTypes.STRING,
    },
    rede_youtube: {               
      type: DataTypes.STRING,
    },
    rede_twitch: {               
      type: DataTypes.STRING,
    },
  },
  {
    timestamps: true,
  },
  {
  },
);

module.exports = User;