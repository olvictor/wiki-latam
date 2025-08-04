const express = require('express');
const { createRole } = require('../controller/Roles');
const app = express.Router();




roles = app.post('/create',createRole)


module.exports = roles;