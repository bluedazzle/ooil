## 工业油必知必会 API

### 首页

```
GET /api/list/
response: {
    status: 0,
    data: [
        {
            id: 0,
            title: 'some title',
            english: 'english title',
            image: 'http://xxx.com/xxx.jpg'
        },
        {
            id: 1,
            title: 'some title',
            english: 'english title',
            image: 'http://xxx.com/xxx.jpg'
        },
        {
            id: 2,
            title: 'some title',
            english: 'english title',
            image: 'http://xxx.com/xxx.jpg'
        }
    ]
}
```

### 详情页

```
GET /api/article/?id=0
response: {
    status: 0,
    data: {
        title: 'some title',
        image: 'http://xxx.com/xxx.jpg',
        content: '<p><span style="color: red">rich</span> text content here</p>'
    }
}
```

### 搜索

```
GET /api/search/?keyword="石油"

response: {
    status: 0,
    data: [
        {
            hint: '石油必知必会',
            id: 0
        },
        {
            hint: '什么是石油',
            id: 1
        }
    ]
}
```