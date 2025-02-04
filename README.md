# genslug

为content/posts里的所有文章，重新生成slug

生成规则是：将字符串“标题|时间的Unix格式”作md5，取前6位

比如

title = "测试 123"
date = "2025-02-04T06:14:09+08:00"

字符串为“测试 123|1738620849”，md5是1ecfe92e64ece1d98939fba4d8d4c634

slug取前6位就是1ecfe9
