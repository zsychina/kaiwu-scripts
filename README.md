# kaiwu 脚本

Author: [siyuan](https://github.com/zsychina)

## 使用方法

1. 下载浏览器对应版本的驱动和Python相关包
2. 替换`config.json`里的`driver_path`，改为自己电脑上的浏览器驱动路径
3. 如果没有`config.json`，请自行创建，格式为

    ```json
    {
        "account": {
            "mail": "",
            "password": ""
        },
        "driver_path": "",
        "opponent_model": "",
        "upload_filter": "",
        "eval_turn": ""
    }
    ```

4. 运行`uploader.py`上传模型，`evaler.py`评估模型，**注意：运行时需要保持浏览器聚焦**

## 进度

- ~~提交模型uploader.py~~
- ~~评估模型evaler.py~~
- ~~根据正则表达式选择模型添加评估~~
