# Auto Game Tools

## 简介

这是一个尝试代替玩家不断循环操作同一个流程的小工具，主要适用于那些操作流程固定，具备自动刷图功能的游戏，如明日方舟，命运之子等。
基于 Python3, PyQt5, opencv 开发。

### 原理

1. 游戏的操作流程固定，这意味着它的操作流程是一个状态机（将每个不同的画面看作一个状态，在不同位置点击看作状态跳转的条件）
2. 用户通过配置界面，建立相应游戏的配置，主要包含状态表以及动作表
3. 根据用户的配置，可以自动判别出当前游戏屏幕的游戏画面是处于什么状态，点击什么位置会前往什么状态
4. 用户给出一个确定运行路径（起点、终点、一个必须包含的中间状态），即可自动寻找路径并自动执行

### 截图

![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/Arknights.png?raw=true)
![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/config.png?raw=true)

## 使用指南

### 游戏状态（State）

游戏状态用来区分当前的游戏界面，通过给定一定[会/不会]出现的子图来判断

* 每个状态最多支持使用三张子图判别，每个子图可以选择在游戏当前画面中出现或者不出现
* 状态有多种类型：
  * normal: 游戏界面不能左右上下移动，所有元素都在一个屏幕范围内
  * jump: 突然出现的游戏界面，比如升级提醒、体力不足提醒、广告等难以判断前一画面是什么
  * horizontal swipe: 需要左右滑动才能将操作区域移动到屏幕内
  * vertical swipe: 需要上下滑动才能将操作区域移动到屏幕内
  * NEED_IDENTIFY: 特殊内置状态，表面需要判断当前状态是什么（比如明日方舟结束界面之后，很难判断下一个画面是什么）

下图表示 LS-3 状态需要图中**出现** Condition LS 以及**不出现** Condition 开始行动

![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/战斗演习.png?raw=true)
![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/config.png?raw=true)

### 游戏动作（Action）

表示一个动作，由 1) 当前状态 2) **点击区域**的图片 3) 操作后第一个识别出的状态 构成

下图表示从 LS-3选中 状态 到 行动配置 状态 需要点击 开始行动区域

![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/action_1.png?raw=true)
![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/LS-3-selected.png?raw=true)

### 运行

需要指定：
1. 游戏配置：游戏名称以及配置名称
2. 运行路径：状态起点->任意一个中间状态->状态终点，如下图

![](https://github.com/SeptemberHX/AutoGameTools/blob/master/screenshot/Arknights.png?raw=true)
