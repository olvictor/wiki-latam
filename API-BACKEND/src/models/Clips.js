
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db_connection');


const Clipes = sequelize.define(
  'Clipes',
  {
    id: {
      type: DataTypes.INTEGER,
      primaryKey:true,
      autoIncrement: true,
    },
    link: {
      type: DataTypes.STRING,
      allowNull:false,
      unique:true,
      validate: {
        notEmpty: {
          msg: "O campo title não pode estar vazio."
        },
        len: {
          args: [3, 255],
          msg: "O título deve ter entre 3 e 255 caracteres."
        },
      }
    },
    aprovado:{
        type:DataTypes.BOOLEAN,
        defaultValue: false
    }
  },
  {
    timestamps: true,
  },
  {
  },
);


module.exports = Clipes;