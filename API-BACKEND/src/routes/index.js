const express = require("express");
const router = express.Router();


const rolesRoutes = require("./role.routes");
const authRoutes = require("./auth.routes");
const postsRoutes = require('./post.routes')

router.use('/role',rolesRoutes);
router.use('/auth',authRoutes);
router.use('/posts',postsRoutes)




module.exports = router;