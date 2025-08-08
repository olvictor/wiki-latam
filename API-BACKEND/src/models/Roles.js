const { DataTypes } = require("sequelize");
const sequelize = require('../config/db_connection');

const Role = sequelize.define("Role", {
  name: { 
    type: DataTypes.STRING, 
    allowNull: false, 
    unique: {
      msg: "Este nome de role já está em uso."
    },
    validate: {
      notEmpty: {
        msg: "O campo name não pode estar vazio."
      },
      len: {
        args: [2, 50],
        msg: "O nome da role deve ter entre 2 e 50 caracteres."
      }
    }
  }
});

module.exports = Role;