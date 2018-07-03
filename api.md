**host: http://oo.chafanbao.com**

**api_version: v1**

#概要

 2. API请求格式：host + "api" + api_version + 请求地址。（eg: http://oo.chafanbao.com/api/v1/articles）
 3. API返回格式：`json:{"status":1,"body":{}}`status返回操作结果码,body包含返回信息，如果无返回信息，body为空。
 4. status结果码对照表：

|status结果码|状态|
| --------------  | :---: |
|0|未知错误|
|1|成功|
|2|权限不足|
|3|帐号不存在|
|4|数据错误|
|5|密码错误|
|6|已存在|
|7|不存在|
|8|已过期|
|10|验证码为空|
|11|验证码错误|


#API认证


 1. 所有请求请带参数 `token={site.slug}` 或 set cookie 用以识别站点信息; eg:http://oo.chafanbao.com/api/v1/articles?token=test

## **获取文章信息**

```
GET /api/v1/articles/
```

### **Parameters**
* token(_Required_|string)-站点
* keyword(_Optional_|string)-搜索内容

### **Return**

#### 说明： 返回数据内 article_type = 0 是文章 article_type = 1 是分类

成功
```
{
    "body":{
        "is_paginated":false,
        "article_list":[
            {
                "picture":"http://ktv.fibar.cn/s/image/avatar.png",
                "title":"一级文章测试",
                "author":"setst",
                "original_create_time":"2018-07-03 11:45:00",
                "belong_id":1,
                "content":"测试内容",
                "article_type":0,
                "create_time":"2018-07-03 11:45:00",
                "modify_time":"2018-07-03 11:46:05",
                "cls_id":null,
                "id":1,
                "priority":0
            },
            {
                "picture":"http://ktv.fibar.cn/s/image/avatar.png",
                "description":"测试分类",
                "title":"测试分类",
                "original_create_time":"2018-07-03 11:45:00",
                "belong_id":1,
                "priority":0,
                "article_type":1,
                "create_time":"2018-07-03 11:45:00",
                "modify_time":"2018-07-03 11:45:30",
                "id":1
            }
        ]
    },
    "status":1,
    "msg":"success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}
```


## **获取分类文章信息**

```
GET /api/v1/classification/{cid}/articles/
```

### **Parameters**
* token(_Required_|string)-站点

### **Return**

成功
```
{
    "body":{
        "article_list":[
            {
                "picture":"http://ktv.fibar.cn/s/image/avatar.png",
                "title":"二级文章测试",
                "author":"测试",
                "original_create_time":"2018-07-03 11:46:00",
                "belong_id":1,
                "content":"二级文章测试内容",
                "article_type":1,
                "create_time":"2018-07-03 11:46:00",
                "modify_time":"2018-07-03 11:47:23",
                "cls_id":1,
                "id":2,
                "priority":0
            }
        ],
        "page_obj":{

        },
        "is_paginated":false
    },
    "status":1,
    "msg":"success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}
```


## **文章详情**

```
GET /api/v1/article/{aid}/
```

### **Parameters**
* token(_Required_|string)-站点

### **Return**

成功
```
{
    "body":{
        "article":{
            "picture":"http://ktv.fibar.cn/s/image/avatar.png",
            "title":"一级文章测试",
            "author":"setst",
            "original_create_time":"2018-07-03 11:45:00",
            "belong_id":1,
            "content":"测试内容",
            "article_type":0,
            "create_time":"2018-07-03 11:45:00",
            "modify_time":"2018-07-03 11:46:05",
            "cls_id":null,
            "id":1,
            "priority":0
        }
    },
    "status":1,
    "msg":"success"
}"msg":"success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}
```