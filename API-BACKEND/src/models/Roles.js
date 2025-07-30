const { DataTypes } = require("sequelize");
const sequelize = require('../config/db_connection');

const Role = sequelize.define("Role", {
  name: { type: DataTypes.STRING, allowNull: false, unique: true }
});

module.exports = Role;