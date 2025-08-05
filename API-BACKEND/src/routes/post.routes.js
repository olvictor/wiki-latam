const express = require('express');
const { cadastrarPost } = require('../controller/Posts');
const { validarLogin } = require('../middleware/auth');
const app = express.Router();



app.use(validarLogin)
posts = app.post('/create',cadastrarPost)


module.exports = posts;