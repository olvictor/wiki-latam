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
      unique:true
    },
    password_hash:{
      type: DataTypes.STRING,
      allowNull:false,
    },
    email:{
      type: DataTypes.STRING,
      unique:true,
      allowNull:false,
    },
  },
  {
    timestamps: true,
  },
  {
  },
);

User.belongsTo(Role, { foreignKey: "role_id" });

module.exports = User;