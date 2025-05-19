const mongoose = require("mongoose");
const Source = require("../models/Source");
const Destination = require("../models/Destination");

// 数据库连接
const BASE_DB = "mongodb://starsnet:password@192.168.3.19/";
const DB_URI = BASE_DB + "copy_shop_config?authSource=admin";

// 示例数据
const sourceData = [
  {
    type: "SHOPIFY",
    base_url: "https://example-shop1.myshopify.com",
  },
  {
    type: "SHOPIFY",
    base_url: "https://example-shop2.myshopify.com",
  },
  {
    type: "SHOPLINE",
    base_url: "https://example-shop3.myshopline.com",
  },
];

const seedDB = async () => {
  try {
    // 连接数据库
    await mongoose.connect(DB_URI);
    console.log("数据库连接成功");

    // 清除现有数据
    await Source.deleteMany({});
    await Destination.deleteMany({});
    console.log("已清除现有数据");

    // 插入源站点数据
    const sources = await Source.insertMany(sourceData);
    console.log("源站点数据已插入");

    // 创建目标站点
    const destination1 = new Destination({
      base_url: "https://our-backend1.example.com",
      source_ids: [sources[0]._id, sources[1]._id],
      markup: 0.3,
    });

    const destination2 = new Destination({
      base_url: "https://our-backend2.example.com",
      source_ids: [sources[2]._id],
      markup: 0.5,
    });

    await Destination.insertMany([destination1, destination2]);
    console.log("目标站点数据已插入");

    console.log("数据库种子数据初始化完成");
    process.exit(0);
  } catch (error) {
    console.error(`错误: ${error.message}`);
    process.exit(1);
  }
};

// 运行种子函数
seedDB();
