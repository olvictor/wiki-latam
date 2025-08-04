const express = require("express");
const router = express.Router();


const rolesRoutes = require("./role.routes");
const authRoutes = require("./auth.routes")


router.use('/role',rolesRoutes);
router.use('/auth',authRoutes);



module.exports = router;