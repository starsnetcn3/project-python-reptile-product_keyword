const axios = require("axios");

const API_URL = "http://127.0.0.1:3008";
const API_TOKEN =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiaWF0IjoxNzQ3Mjk1NDI4LCJleHAiOjE3NDc5MDAyMjh9.fo4HKZWkxnLO1Du5oncvvyhHLab1J49lIQjrN8_0818";

const SHOP_PRODUCT = [
  {
    id: 8106128179386,
    title: "Hemp Laurel Romper",
    handle: "hemp-laurel-romper-oasis-peony",
    body_html:
      "<p>Name a style that says summer fun more than a flowy romper — we'll wait. With adjustable spaghetti straps in our breathable Hemp Tencel fabric, embrace whatever the day brings in the Laurel Romper.</p>",
    product_type: "Womens",
    variants: [
      {
        id: 44740212162746,
        title: "OASIS PEONY / 2",
        option1: "OASIS PEONY",
        option2: "2",
        option3: null,
        sku: "TCW6190-5319-2",
        requires_shipping: true,
        taxable: true,
        featured_image: {
          id: 37949353951418,
          product_id: 8106128179386,
          position: 1,
          created_at: "2025-03-27T16:57:30-07:00",
          updated_at: "2025-03-27T16:57:31-07:00",
          alt: "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
          width: 960,
          height: 1200,
          src: "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
          variant_ids: [
            44740212162746, 44740212195514, 44740212228282, 44740212261050,
            44740212293818, 44740212326586, 44740212359354,
          ],
        },
        available: true,
        price: "98.00",
        grams: 800,
        compare_at_price: null,
        position: 1,
        product_id: 8106128179386,
        created_at: "2025-03-27T16:57:21-07:00",
        updated_at: "2025-05-16T00:07:15-07:00",
      },
      // 其他变体数据 (简化展示，实际中保留所有数据)
    ],
    images: [
      {
        id: 37949353951418,
        created_at: "2025-03-27T16:57:30-07:00",
        position: 1,
        updated_at: "2025-03-27T16:57:31-07:00",
        product_id: 8106128179386,
        variant_ids: [
          44740212162746, 44740212195514, 44740212228282, 44740212261050,
          44740212293818, 44740212326586, 44740212359354,
        ],
        src: "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
        width: 960,
        height: 1200,
      },
      // 其他图片数据 (简化展示，实际中保留所有数据)
    ],
  },
  {
    id: 8106128113850,
    title: "Hemp Laurel Romper",
    handle: "hemp-laurel-romper-agave-green",
    body_html:
      "<p>Name a style that says summer fun more than a flowy romper — we'll wait. With adjustable spaghetti straps in our breathable Hemp Tencel fabric, embrace whatever the day brings in the Laurel Romper.</p>",
    published_at: "2025-04-02T10:47:54-07:00",
    created_at: "2025-03-27T16:57:18-07:00",
    updated_at: "2025-05-16T00:07:15-07:00",
    vendor: "tentree",
    product_type: "Womens",
    tags: [
      "bday-sale-SS25-20",
      "dresses-jumpsuits",
      "favourites",
      "FW24-SS25",
      "gh-womens-hemp-laurel-romper-sunray-peony",
      "hemp",
      "jumpsuit",
      "online-whs",
      "organic-cotton",
      "points_10",
      "romper",
      "SP25-faves",
      "SS25",
      "SU25",
      "SU25-new-style",
      "SU25-summer-launch",
      "supercircle",
      "tencel",
      "tops",
      "w",
      "womens",
    ],
    variants: [
      {
        id: 44740211769530,
        title: "AGAVE GREEN / 2",
        option1: "AGAVE GREEN",
        option2: "2",
        option3: null,
        sku: "TCW6190-1480-2",
        requires_shipping: true,
        taxable: true,
        featured_image: {
          id: 37949352968378,
          product_id: 8106128113850,
          position: 1,
          created_at: "2025-03-27T16:57:26-07:00",
          updated_at: "2025-03-27T16:57:28-07:00",
          alt: "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
          width: 960,
          height: 1200,
          src: "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
          variant_ids: [
            44740211769530, 44740211802298, 44740211835066, 44740211867834,
            44740211900602, 44740211933370, 44740211966138,
          ],
        },
        available: true,
        price: "98.00",
        grams: 800,
        compare_at_price: null,
        position: 1,
        product_id: 8106128113850,
        created_at: "2025-03-27T16:57:18-07:00",
        updated_at: "2025-05-16T00:07:15-07:00",
      },
      // 其他变体数据 (简化展示，实际中保留所有数据)
    ],
    images: [
      // 图片数据 (简化展示，实际中保留所有数据)
    ],
    options: [
      {
        name: "Color",
        position: 1,
        values: ["AGAVE GREEN"],
      },
      {
        name: "Size",
        position: 2,
        values: ["2", "4", "6", "8", "10", "12", "14"],
      },
    ],
  },
];

// 创建HTTP请求头
const createHeaders = () => {
  return {
    Authorization: `Bearer ${API_TOKEN}`,
    "Content-Type": "application/json",
  };
};

const insert_data = async (data) => {
  data.map(async (product_item) => {
    const product_item_id = product_item.id;
    //通过shopify 的id去mongodb里面查询all的product
    const all_product_data = await axios.get(`${API_URL}/common/all/MProduct`, {
      headers: createHeaders(),
      params: {
        shopify_product_id: {
          $in: [product_item_id.toString()],
        },
      },
    });
    // 1. 插入新的产品
    if (!all_product_data.data.data.length) {
      console.log("===insert product id ", product_item_id);
      //插入产品
      const insert_product = await axios.post(
        `${API_URL}/common/create/MProduct`,
        {
          shopify_product_id: product_item_id.toString(),
          title: {
            en: product_item.title,
            zh: product_item.title,
            cn: product_item.title,
          },
          short_description: {
            en: product_item.handle,
            zh: product_item.handle,
            cn: product_item.handle,
          },
          long_description: {
            en: product_item.body_html,
            zh: product_item.body_html,
            cn: product_item.body_html,
          },
          status: "ACTIVE",
          shopify_link: "",
          images: product_item.images.map((item) => item.src),
        },
        {
          headers: createHeaders(),
        }
      );

      //插入的product_id
      const insert_product_id = insert_product.data.data._id;

      //插入产品变体
      product_item.variants.map(async (variant_item) => {
        console.log("======insert variant id ", variant_item.id);
        await axios.post(
          `${API_URL}/common/create/MProductVariant`,
          {
            product_id: insert_product_id,
            shopify_product_variant_id: variant_item.id.toString(),
            title: {
              en: variant_item.title,
              zh: variant_item.title,
              cn: variant_item.title,
            },
            short_description: {
              en: product_item.handle,
              zh: product_item.handle,
              cn: product_item.handle,
            },
            long_description: {
              en: product_item.body_html,
              zh: product_item.body_html,
              cn: product_item.body_html,
            },
            price: Number(variant_item.price),
            status: "ACTIVE",
            shopify_link: "",
            images: [variant_item?.featured_image?.src],
          },
          { headers: createHeaders() }
        );
      });
    }
    // 2. 更新产品
    else {
      console.log("===update product id ", product_item_id);
      //通过shopify_id去查找需要更新的产品id
      const get_one_product = await axios.get(
        `${API_URL}/common/all/MProduct`,
        {
          headers: createHeaders(),
          params: {
            shopify_product_id: {
              $in: [product_item_id.toString()],
            },
          },
        }
      );

      //拿到需要更新的产品id
      const update_product_id = get_one_product.data.data[0]._id;

      //更新产品
      await axios.put(
        `${API_URL}/common/update/${update_product_id}/MProduct`,
        {
          title: {
            en: product_item.title,
            zh: product_item.title,
            cn: product_item.title,
          },
          short_description: {
            en: product_item.handle,
            zh: product_item.handle,
            cn: product_item.handle,
          },
          long_description: {
            en: product_item.body_html,
            zh: product_item.body_html,
            cn: product_item.body_html,
          },
          status: "ACTIVE",
          shopify_link: "",
          images: product_item.images.map((item) => item.src),
        },
        {
          headers: createHeaders(),
        }
      );

      //更新产品变体
      product_item.variants.map(async (variant_item) => {
        console.log("======update variant id ", variant_item.id);
        //通过shopify_id去查找需要更新的产品变体id
        const get_one_variant = await axios.get(
          `${API_URL}/common/all/MProductVariant`,
          {
            headers: createHeaders(),
            params: {
              shopify_product_variant_id: {
                $in: [variant_item.id.toString()],
              },
            },
          }
        );

        //拿到需要更新的产品变体id
        const update_variant_id = get_one_variant.data.data[0]._id;

        await axios.put(
          `${API_URL}/common/update/${update_variant_id}/MProductVariant`,
          {
            title: {
              en: variant_item.title,
              zh: variant_item.title,
              cn: variant_item.title,
            },
            short_description: {
              en: product_item.handle,
              zh: product_item.handle,
              cn: product_item.handle,
            },
            long_description: {
              en: product_item.body_html,
              zh: product_item.body_html,
              cn: product_item.body_html,
            },
            price: Number(variant_item.price),
            status: "ACTIVE",
            shopify_link: "",
            images: [variant_item?.featured_image?.src],
          },
          { headers: createHeaders() }
        );
      });
    }
  });
  // 3. 删除产品
  //获取数据库的全部产品id
  const all_product_id = await axios.get(`${API_URL}/common/all/MProduct`, {
    headers: createHeaders(),
  });

  //获取数据库的全部产品id
  const all_shopify_product_id_list = all_product_id.data.data.map((item) => {
    return {
      id: item.shopify_product_id,
      _id: item._id,
    };
  });

  //获取shopify的全部产品id
  const shopify_product_id_list = SHOP_PRODUCT;

  //获取需要删除的product
  const difference = all_shopify_product_id_list.filter(
    (obj1) =>
      !shopify_product_id_list.some((obj2) => String(obj2.id) === obj1.id)
  );

  //需要删除的产品id
  const delete_product_id_list = difference.map((item) => item._id);

  console.log("===delete_product_id_list", delete_product_id_list);

  //删除不存在的产品
  if (delete_product_id_list.length) {
    //删除产品
    await axios.delete(`${API_URL}/common/delete/MProduct`, {
      headers: createHeaders(),
      data: {
        targetIds: delete_product_id_list,
      },
    });
    //获取需要删除的产品变体
    const all_product_variant_id = await axios.get(
      `${API_URL}/common/all/MProductVariant`,
      {
        headers: createHeaders(),
        params: {
          product_id: {
            $in: delete_product_id_list,
          },
        },
      }
    );
    //获取需要删除的产品变体id
    const delete_product_variant_id_list = all_product_variant_id.data.data.map(
      (item) => item._id
    );
    console.log(
      "===delete_product_variant_id_list",
      delete_product_variant_id_list
    );
    //删除产品变体
    await axios.delete(`${API_URL}/common/delete/MProductVariant`, {
      headers: createHeaders(),
      data: {
        targetIds: delete_product_variant_id_list,
      },
    });
  }
};

// 开始定时器
const startTimer = (interval) => {
  console.log(`开始定时任务，每${interval}秒执行一次`);

  // 立即执行一次
  console.log(`开始执行 insert() at ${new Date().toISOString()}`);
  insert_data(SHOP_PRODUCT);

  // 设置定时器
  setInterval(() => {
    console.log(`开始执行 fetchData() at ${new Date().toISOString()}`);
    insert_data(SHOP_PRODUCT);
  }, interval * 1000);
};

// 主函数
const main = () => {
  const interval = 10; // 每隔10秒获取一次数据
  startTimer(interval);
};

// 启动程序
main();
