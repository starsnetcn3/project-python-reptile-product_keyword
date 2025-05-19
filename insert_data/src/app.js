const express = require("express");
const cors = require("cors");
const connectDB = require("./config/db");

// 预加载所有模型，确保Mongoose能够正确引用它们
require("./models/Source");
require("./models/Destination");

// 连接数据库
connectDB();

const app = express();

// 中间件
app.use(cors());
app.use(express.json());

// 路由
app.use("/api/destinations", require("./routes/destinationRoutes"));

// 首页路由
app.get("/", (req, res) => {
  res.json({ message: "欢迎使用 Copy Shop API" });
});

// 端口设置
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
});

module.exports = app;
