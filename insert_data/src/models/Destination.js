const mongoose = require("mongoose");

const DestinationSchema = new mongoose.Schema(
  {
    base_url: {
      type: String,
      required: true,
    },
    source_ids: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Source",
      },
    ],
    markup: {
      type: Number,
      required: true,
    },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

module.exports = mongoose.model("Destination", DestinationSchema);
