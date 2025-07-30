const express = require('express');
const Role = require('../models/Roles');
const { createRole } = require('../controller/Roles');
const app = express.Router();




role = app.post('/roles',createRole)


module.exports = role;