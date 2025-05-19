const express = require("express");
const router = express.Router();
const { getDestinations } = require("../controllers/destinationController");

// 获取所有目标站点
router.get("/", getDestinations);

module.exports = router;
