import threading
import time
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:3008"
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiaWF0IjoxNzQ3Mjk1NDI4LCJleHAiOjE3NDc5MDAyMjh9.fo4HKZWkxnLO1Du5oncvvyhHLab1J49lIQjrN8_0818"

SHOP = [
    {
        "id": 8106128179386,
        "title": "Hemp Laurel Romper",
        "handle": "hemp-laurel-romper-oasis-peony",
        "body_html": "<p>Name a style that says summer fun more than a flowy romper — we’ll wait. With adjustable spaghetti straps in our breathable Hemp Tencel fabric, embrace whatever the day brings in the Laurel Romper.</p>",
        "product_type": "Womens",
        "variants": [
            {
                "id": 44740212162746,
                "title": "OASIS PEONY / 2",
                "option1": "OASIS PEONY",
                "option2": "2",
                "option3": null,
                "sku": "TCW6190-5319-2",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 1,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740212195514,
                "title": "OASIS PEONY / 4",
                "option1": "OASIS PEONY",
                "option2": "4",
                "option3": null,
                "sku": "TCW6190-5319-4",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 2,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740212228282,
                "title": "OASIS PEONY / 6",
                "option1": "OASIS PEONY",
                "option2": "6",
                "option3": null,
                "sku": "TCW6190-5319-6",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 3,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740212261050,
                "title": "OASIS PEONY / 8",
                "option1": "OASIS PEONY",
                "option2": "8",
                "option3": null,
                "sku": "TCW6190-5319-8",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 4,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740212293818,
                "title": "OASIS PEONY / 10",
                "option1": "OASIS PEONY",
                "option2": "10",
                "option3": null,
                "sku": "TCW6190-5319-10",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 5,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740212326586,
                "title": "OASIS PEONY / 12",
                "option1": "OASIS PEONY",
                "option2": "12",
                "option3": null,
                "sku": "TCW6190-5319-12",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 6,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740212359354,
                "title": "OASIS PEONY / 14",
                "option1": "OASIS PEONY",
                "option2": "14",
                "option3": null,
                "sku": "TCW6190-5319-14",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949353951418,
                    "product_id": 8106128179386,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:30-07:00",
                    "updated_at": "2025-03-27T16:57:31-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                    "variant_ids": [
                        44740212162746,
                        44740212195514,
                        44740212228282,
                        44740212261050,
                        44740212293818,
                        44740212326586,
                        44740212359354
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 7,
                "product_id": 8106128179386,
                "created_at": "2025-03-27T16:57:21-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            }
        ],
        "images": [
            {
                "id": 37949353951418,
                "created_at": "2025-03-27T16:57:30-07:00",
                "position": 1,
                "updated_at": "2025-03-27T16:57:31-07:00",
                "product_id": 8106128179386,
                "variant_ids": [
                    44740212162746,
                    44740212195514,
                    44740212228282,
                    44740212261050,
                    44740212293818,
                    44740212326586,
                    44740212359354
                ],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_5.jpg?v=1743119851",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949354082490,
                "created_at": "2025-03-27T16:57:30-07:00",
                "position": 2,
                "updated_at": "2025-03-27T16:57:31-07:00",
                "product_id": 8106128179386,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_4.jpg?v=1743119851",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949354016954,
                "created_at": "2025-03-27T16:57:30-07:00",
                "position": 3,
                "updated_at": "2025-03-27T16:57:31-07:00",
                "product_id": 8106128179386,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_2.jpg?v=1743119851",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949354049722,
                "created_at": "2025-03-27T16:57:30-07:00",
                "position": 4,
                "updated_at": "2025-03-27T16:57:31-07:00",
                "product_id": 8106128179386,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_3.jpg?v=1743119851",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949353984186,
                "created_at": "2025-03-27T16:57:30-07:00",
                "position": 5,
                "updated_at": "2025-03-27T16:57:31-07:00",
                "product_id": 8106128179386,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-5319_1.jpg?v=1743119851",
                "width": 960,
                "height": 1200
            }
        ],
    },

    {
        "id": 8106128113850,
        "title": "Hemp Laurel Romper",
        "handle": "hemp-laurel-romper-agave-green",
        "body_html": "<p>Name a style that says summer fun more than a flowy romper — we’ll wait. With adjustable spaghetti straps in our breathable Hemp Tencel fabric, embrace whatever the day brings in the Laurel Romper.</p>",
        "published_at": "2025-04-02T10:47:54-07:00",
        "created_at": "2025-03-27T16:57:18-07:00",
        "updated_at": "2025-05-16T00:07:15-07:00",
        "vendor": "tentree",
        "product_type": "Womens",
        "tags": [
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
            "womens"
        ],
        "variants": [
            {
                "id": 44740211769530,
                "title": "AGAVE GREEN / 2",
                "option1": "AGAVE GREEN",
                "option2": "2",
                "option3": null,
                "sku": "TCW6190-1480-2",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 1,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740211802298,
                "title": "AGAVE GREEN / 4",
                "option1": "AGAVE GREEN",
                "option2": "4",
                "option3": null,
                "sku": "TCW6190-1480-4",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 2,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740211835066,
                "title": "AGAVE GREEN / 6",
                "option1": "AGAVE GREEN",
                "option2": "6",
                "option3": null,
                "sku": "TCW6190-1480-6",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 3,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740211867834,
                "title": "AGAVE GREEN / 8",
                "option1": "AGAVE GREEN",
                "option2": "8",
                "option3": null,
                "sku": "TCW6190-1480-8",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 4,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740211900602,
                "title": "AGAVE GREEN / 10",
                "option1": "AGAVE GREEN",
                "option2": "10",
                "option3": null,
                "sku": "TCW6190-1480-10",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 5,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740211933370,
                "title": "AGAVE GREEN / 12",
                "option1": "AGAVE GREEN",
                "option2": "12",
                "option3": null,
                "sku": "TCW6190-1480-12",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 6,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            },
            {
                "id": 44740211966138,
                "title": "AGAVE GREEN / 14",
                "option1": "AGAVE GREEN",
                "option2": "14",
                "option3": null,
                "sku": "TCW6190-1480-14",
                "requires_shipping": true,
                "taxable": true,
                "featured_image": {
                    "id": 37949352968378,
                    "product_id": 8106128113850,
                    "position": 1,
                    "created_at": "2025-03-27T16:57:26-07:00",
                    "updated_at": "2025-03-27T16:57:28-07:00",
                    "alt": "Green-Relaxed-Fit-Button-Front-A-Line-Romper",
                    "width": 960,
                    "height": 1200,
                    "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                    "variant_ids": [
                        44740211769530,
                        44740211802298,
                        44740211835066,
                        44740211867834,
                        44740211900602,
                        44740211933370,
                        44740211966138
                    ]
                },
                "available": true,
                "price": "98.00",
                "grams": 800,
                "compare_at_price": null,
                "position": 7,
                "product_id": 8106128113850,
                "created_at": "2025-03-27T16:57:18-07:00",
                "updated_at": "2025-05-16T00:07:15-07:00"
            }
        ],
        "images": [
            {
                "id": 37949352968378,
                "created_at": "2025-03-27T16:57:26-07:00",
                "position": 1,
                "updated_at": "2025-03-27T16:57:28-07:00",
                "product_id": 8106128113850,
                "variant_ids": [
                    44740211769530,
                    44740211802298,
                    44740211835066,
                    44740211867834,
                    44740211900602,
                    44740211933370,
                    44740211966138
                ],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_4.jpg?v=1743119848",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949352935610,
                "created_at": "2025-03-27T16:57:26-07:00",
                "position": 2,
                "updated_at": "2025-03-27T16:57:28-07:00",
                "product_id": 8106128113850,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_3.jpg?v=1743119848",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949352902842,
                "created_at": "2025-03-27T16:57:26-07:00",
                "position": 3,
                "updated_at": "2025-03-27T16:57:27-07:00",
                "product_id": 8106128113850,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_1.jpg?v=1743119847",
                "width": 960,
                "height": 1200
            },
            {
                "id": 37949353001146,
                "created_at": "2025-03-27T16:57:26-07:00",
                "position": 4,
                "updated_at": "2025-03-27T16:57:28-07:00",
                "product_id": 8106128113850,
                "variant_ids": [],
                "src": "https://cdn.shopify.com/s/files/1/2341/3995/files/Green-Relaxed-Fit-Button-Front-A-Line-Romper-TCW6190-1480_2.jpg?v=1743119848",
                "width": 960,
                "height": 1200
            }
        ],
        "options": [
            {
                "name": "Color",
                "position": 1,
                "values": [
                    "AGAVE GREEN"
                ]
            },
            {
                "name": "Size",
                "position": 2,
                "values": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14"
                ]
            }
        ]
    },

]

def fetch_data():

    all_product_data = get_all_product_data()
    all_product_variant_data = get_all_product_variant_data()
    # 数据库没有数据直插入
    if(0 == len(all_product_data['data']) or 0 == len(all_product_variant_data['data'])):
        if(0 == len(all_product_data['data'])):
            for product in products:
                insert_product_data(product)
        if(0 == len(all_product_variant_data['data'])):
            for product_variant in product_variants:
                insert_product_variant_data(product_variant)
    else:
        all_product_data_id = [obj['_id'] for obj in all_product_data["data"] ]
        all_product_data_variant_id = [obj['_id'] for obj in all_product_variant_data["data"] ]
        print("all product id")
        print(all_product_data_id)
        print("all product variant id")
        print(all_product_data_variant_id)
        # 检测机制
        ## product
        ### 1. 插入新的产品
        for product in products:
            if product['_id'] not in all_product_data_id:
                print(f"insert product_id:{product['_id']}")
                insert_product_data(product)  # 插入新产品
            else:
                print(f"update product_id:{product['_id']}")
                update_product_data(product)   # 更新已有产品

        ### 3. 删除不存在的产品
        for product_id in all_product_data_id:
            if not any(product['_id'] == product_id for product in products):
                print(f"delete product_id:{product_id}")
                delete_product_data(product_id)

        ## product_variant
        ### 1. 插入新的产品变体
        for product_variant in product_variants:
            if product_variant['_id'] not in all_product_data_variant_id:
                print(f"insert product_variant_id:{product_variant['_id']}")
                insert_product_variant_data(product_variant)
            else:
                print(f"update product_variant_id:{product_variant['_id']}")
                update_product_variant_data(product_variant)
            
        ### 3. 删除不存在的产品变体
        for product_variant_id in all_product_data_variant_id:
            if not any(product_variant_id == product_variant['_id'] for product_variant in product_variants):
                print(f"delete product_variant_id:{product_variant_id}")
                delete_product_variant_data(product_variant_id)

def get_all_product_data():
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(API_URL+"/common/all/MProduct", headers=headers)

        # 检查响应状态
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def get_all_product_variant_data():
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(API_URL+"/common/all/MProductVariant", headers=headers)

        # 检查响应状态
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def insert_product_data(data):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(API_URL+"/common/create/MProduct", headers=headers, json=data)

        # 检查响应状态
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def insert_product_variant_data(data):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(API_URL+"/common/create/MProductVariant", headers=headers, json=data)

        # 检查响应状态
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def update_product_data(data):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    update_id = data['_id']
    try:
        response = requests.put(API_URL+f'/common/update/{update_id}/MProduct', headers=headers, json=data)
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def update_product_variant_data(data):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    update_id = data['_id']
    try:
        response = requests.put(API_URL+f'/common/update/{update_id}/MProductVariant', headers=headers, json=data)
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def delete_product_data(data):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    json_data = {"targetIds":[data]}
    try:
        response = requests.delete(API_URL+'/common/delete/MProduct', headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def delete_product_variant_data(data):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    json_data = {"targetIds":[data]}
    try:
        response = requests.delete(API_URL+'/common/delete/MProductVariant', headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

def start_timer(interval):
    while True:
        print("开始执行 fetch_data() at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fetch_data()
        time.sleep(interval)  # 设置间隔时间


if __name__ == "__main__":
    interval = 10  # 每隔10秒获取一次数据
    timer_thread = threading.Thread(target=start_timer, args=(interval,))
    timer_thread.start()