# Copy Shop API

一个基于 Express 和 MongoDB 的 RESTful API 服务，用于管理复制商店的数据。

## 功能

- 获取所有目标站点及其关联的源站点

## 技术栈

- Node.js
- Express
- MongoDB
- Mongoose

## 安装

```bash
# 安装依赖
npm install

# 开发模式运行
npm run dev

# 生产模式运行
npm start
```

## API 文档

### 获取所有目标站点

```
GET /api/destinations
```

响应示例:

```json
[
  {
    "_id": "ObjectId",
    "base_url": "后端地址",
    "source_arr": [
      {
        "_id": "ObjectId",
        "type": "SHOPIFY",
        "base_url": "要爬的shopify地址"
      }
    ],
    "markup": 0.5
  }
]
```
