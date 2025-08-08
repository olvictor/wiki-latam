const { DataTypes } = require('sequelize');
const sequelize = require('../config/db_connection');
const Role = require('../models/Roles')

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
        len: {
          args: [3, 50],
          msg: "O nome de usuário deve ter entre 3 e 50 caracteres."
        }
      }
    },
    password_hash:{
      type: DataTypes.STRING,
      allowNull:false,
      validate: {
        notEmpty: {
          msg: "O campo password não pode estar vazio."
        }
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
      }
    }
  },
  {
    timestamps: true,
  },
  {
  },
);

User.belongsTo(Role, { foreignKey: "role_id" });

module.exports = User;