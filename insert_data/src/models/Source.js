const mongoose = require("mongoose");

const SourceSchema = new mongoose.Schema(
  {
    type: {
      type: String,
      enum: ["SHOPIFY", "SHOPLINE"],
      required: true,
    },
    base_url: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

module.exports = mongoose.model("Source", SourceSchema);
