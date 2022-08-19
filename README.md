# DjangoWebsite
## 项目主要功能
  该系统主要分为股票预测模型、Web 构建两个技术方向。对于股票 预测模型，采用在金融界广受好评的LSTM预测模型。在此基础上，将模 型的相关手动操作改良为自动化操作。对于Web构建，则采用具备完整网站配置的DjangoWeb框架，避免框架漏洞。并在此基础上利用 Django 的视图模块，隐 式实现调用爬虫接口、股票预测接口的操作，使用户的操作简易化。
在众多深度神经网络模型中，LSTM 模型被广泛应用于各种时间序列分析任务中。同时，对比其他预测模型，LSTM 模型在金融市场预测中有较高的权威。因此，本项目采用LSTM时序模型。

<img width="338" alt="image" src="https://user-images.githubusercontent.com/61780819/178501780-069508a9-cb51-49c0-818e-4ed2e70f6eb0.png">

## 项目展示
本团队通过随机抽样的方式，选定股票号为000333、601857、300435、000671进行模型预测，得到最大预测误差为5.61%，最低误差为2.26%的测试结果（见图）。

<img width="254" alt="image" src="https://user-images.githubusercontent.com/61780819/178502385-192fb3b8-dc46-4bea-a322-d2a167dda64c.png">

同时，通过模型拟合情况图可以认为，预测误差低于10%，且拟合状况良好，准确性较优，可以认为具有有效性。
 
 <img width="278" alt="image" src="https://user-images.githubusercontent.com/61780819/178502402-e1809cf5-8add-425e-b9d7-f1c3ae39ddb4.png">

## 项目图示

<img width="1168" alt="image" src="https://user-images.githubusercontent.com/61780819/178503642-23028bd3-6a7e-4844-8c96-39ac3298db4e.png">


<img width="1278" alt="image" src="https://user-images.githubusercontent.com/61780819/178503311-320bcd0c-2c9a-4491-a223-c687e9dc37b2.png">



