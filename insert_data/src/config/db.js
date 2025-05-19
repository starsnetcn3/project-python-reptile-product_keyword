const mongoose = require("mongoose");

const BASE_DB = "mongodb://starsnet:password@192.168.3.19/";
const DB_URI = BASE_DB + "copy_shop_config?authSource=admin";

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(DB_URI);
    console.log(`MongoDB 连接成功: ${conn.connection.host}`);
  } catch (error) {
    console.error(`MongoDB 连接错误: ${error.message}`);
    process.exit(1);
  }
};

module.exports = connectDB;
