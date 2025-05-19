const Destination = require("../models/Destination");

// 获取所有目标站点及其关联的源站点
exports.getDestinations = async (req, res) => {
  try {
    const destinations = await Destination.find().populate({
      path: "source_ids",
      select: "_id type base_url",
    });

    // 按照需要的格式转换数据
    const formattedDestinations = destinations.map((dest) => {
      return {
        _id: dest._id,
        base_url: dest.base_url,
        source_arr: dest.source_ids.map((source) => ({
          _id: source._id,
          type: source.type,
          base_url: source.base_url,
        })),
        markup: dest.markup,
      };
    });

    res.json(formattedDestinations);
  } catch (error) {
    console.error(`获取目标站点失败: ${error.message}`);
    res.status(500).json({ message: "服务器错误" });
  }
};
