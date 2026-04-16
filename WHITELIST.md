# 网站白名单配置指南

## 🎯 解决误判问题

如果某些网站或应用被误判为广告导致无法正常使用，请按照以下步骤添加白名单。

---

## ⚡ 快速添加白名单

### 方法 1：直接编辑配置文件（推荐）

1. **打开配置文件** `data/config.yaml`

2. **找到白名单部分**（第 130-140 行）：
   ```yaml
   rules:
     # ========== 白名单规则（必须放在最前面）==========
     # 如果某些网站被误判为广告，在这里添加白名单规则
     # 格式：- DOMAIN-SUFFIX，域名，DIRECT
     
     # 示例白名单（根据需要取消注释并修改）
     # - DOMAIN-SUFFIX,example.com,DIRECT
     # - DOMAIN-SUFFIX,mysite.com,DIRECT
   ```

3. **取消注释并修改**，例如：
   ```yaml
   rules:
     # 白名单规则
     - DOMAIN-SUFFIX,example.com,DIRECT
     - DOMAIN-SUFFIX,mysite.com,DIRECT
     - DOMAIN-SUFFIX,github.com,DIRECT
     
     # 广告拦截规则...
   ```

4. **保存并推送**到 GitHub

---

### 方法 2：创建独立白名单文件

1. **创建白名单文件** `data/rule_providers/whitelist.yaml`：
   ```yaml
   payload:
     - DOMAIN-SUFFIX,example.com
     - DOMAIN-SUFFIX,mysite.com
     - DOMAIN,specific-page.com
   ```

2. **编辑配置文件** `data/config.yaml`，添加规则提供者：
   ```yaml
   rule-providers:
     Whitelist:
       type: file
       behavior: classical
       format: yaml
       path: ./rule_providers/whitelist.yaml
   ```

3. **在 rules 部分引用**（必须放在最前面）：
   ```yaml
   rules:
     - RULE-SET,Whitelist,DIRECT
     
     # 其他规则...
   ```

---

## 📝 白名单规则语法

### 规则格式

```yaml
- DOMAIN-SUFFIX，域名，DIRECT    # 域名后缀匹配
- DOMAIN，完整域名，DIRECT        # 域名完全匹配
- DOMAIN-KEYWORD，关键字，DIRECT  # 域名关键字匹配
- IP-CIDR,IP 段，DIRECT          # IP 地址段匹配
```

### 常用示例

#### 1. 整个域名白名单（推荐）
```yaml
- DOMAIN-SUFFIX,example.com,DIRECT
```
这会允许 `example.com` 及其所有子域名（如 `www.example.com`、`api.example.com`）

#### 2. 特定域名白名单
```yaml
- DOMAIN,www.example.com,DIRECT
```
只允许 `www.example.com`，不包括其他子域名

#### 3. 关键字白名单
```yaml
- DOMAIN-KEYWORD,mycompany,DIRECT
```
允许所有包含 `mycompany` 的域名

#### 4. IP 地址白名单
```yaml
- IP-CIDR,192.168.1.0/24,DIRECT
```

---

## 🔍 常见误判场景

### 场景 1：网站功能异常

**症状**：
- 网站部分功能无法使用
- 图片、视频加载失败
- API 请求被拦截

**解决方案**：
```yaml
rules:
  # 添加整个域名到白名单
  - DOMAIN-SUFFIX,example.com,DIRECT
  
  # 或者只添加特定的 CDN 域名
  - DOMAIN-SUFFIX,cdn.example.com,DIRECT
  - DOMAIN-SUFFIX,static.example.com,DIRECT
```

### 场景 2：应用无法联网

**症状**：
- 手机应用提示网络错误
- 应用内容无法加载
- 登录失败

**解决方案**：
```yaml
rules:
  # 查找应用的 API 域名并添加
  - DOMAIN-SUFFIX,api.example.com,DIRECT
  - DOMAIN-SUFFIX,services.example.com,DIRECT
```

### 场景 3：开发/测试环境被拦截

**症状**：
- 本地开发环境无法访问
- 测试 API 被拦截

**解决方案**：
```yaml
rules:
  # 本地开发环境
  - DOMAIN-KEYWORD,localhost,DIRECT
  - IP-CIDR,127.0.0.1/8,DIRECT
  
  # 测试环境
  - DOMAIN-SUFFIX,test.example.com,DIRECT
  - DOMAIN-SUFFIX,staging.example.com,DIRECT
```

### 场景 4：特定服务被误判

**症状**：
- 推送通知无法接收
- 第三方登录失败
- 支付功能异常

**解决方案**：
```yaml
rules:
  # 推送服务
  - DOMAIN-SUFFIX,firebase.google.com,DIRECT
  - DOMAIN-SUFFIX,xmpp.google.com,DIRECT
  
  # 第三方登录
  - DOMAIN-SUFFIX,graph.facebook.com,DIRECT
  - DOMAIN-SUFFIX,api.twitter.com,DIRECT
  
  # 支付服务
  - DOMAIN-SUFFIX,paypal.com,DIRECT
  - DOMAIN-SUFFIX,stripe.com,DIRECT
```

---

## 🛠️ 排查误判问题

### 步骤 1：查看日志

在 Clash Meta 中查看被拦截的请求：

1. 打开 Clash Meta 应用
2. 进入「日志」或「Logs」
3. 筛选 `REJECT` 或 `DROP` 级别的日志
4. 找到被拦截的域名

### 步骤 2：测试验证

临时添加规则并测试：

```yaml
rules:
  # 临时测试规则
  - DOMAIN-SUFFIX,problem-site.com,DIRECT
  
  # 其他规则...
```

### 步骤 3：确认解决

- 访问问题网站，确认功能正常
- 检查日志，确认请求已直连

---

## 📋 常用白名单参考

### 国内常用服务

```yaml
rules:
  # 微信相关
  - DOMAIN-SUFFIX,wechat.com,DIRECT
  - DOMAIN-SUFFIX,weixin.qq.com,DIRECT
  
  # 支付宝
  - DOMAIN-SUFFIX,alipay.com,DIRECT
  - DOMAIN-SUFFIX,alipayobjects.com,DIRECT
  
  # 淘宝/天猫
  - DOMAIN-SUFFIX,taobao.com,DIRECT
  - DOMAIN-SUFFIX,tmall.com,DIRECT
  
  # 百度
  - DOMAIN-SUFFIX,baidu.com,DIRECT
  - DOMAIN-SUFFIX,bdstatic.com,DIRECT
  
  # 腾讯
  - DOMAIN-SUFFIX,qq.com,DIRECT
  - DOMAIN-SUFFIX,tencent.com,DIRECT
  
  # 阿里
  - DOMAIN-SUFFIX,alibaba.com,DIRECT
  - DOMAIN-SUFFIX,aliyuncs.com,DIRECT
  
  # 小米
  - DOMAIN-SUFFIX,mi.com,DIRECT
  - DOMAIN-SUFFIX,miui.com,DIRECT
  
  # 华为
  - DOMAIN-SUFFIX,huawei.com,DIRECT
  - DOMAIN-SUFFIX,hicloud.com,DIRECT
```

### 国际常用服务

```yaml
rules:
  # Google 服务（如果你需要访问）
  - DOMAIN-SUFFIX,google.com,DIRECT
  - DOMAIN-SUFFIX,googleapis.com,DIRECT
  
  # GitHub
  - DOMAIN-SUFFIX,github.com,DIRECT
  - DOMAIN-SUFFIX,githubusercontent.com,DIRECT
  
  # Microsoft
  - DOMAIN-SUFFIX,microsoft.com,DIRECT
  - DOMAIN-SUFFIX,windows.com,DIRECT
  
  # Apple
  - DOMAIN-SUFFIX,apple.com,DIRECT
  - DOMAIN-SUFFIX,icloud.com,DIRECT
  
  # Amazon
  - DOMAIN-SUFFIX,amazon.com,DIRECT
  - DOMAIN-SUFFIX,aws.amazon.com,DIRECT
```

### 开发相关

```yaml
rules:
  # 开发工具
  - DOMAIN-SUFFIX,npmjs.com,DIRECT
  - DOMAIN-SUFFIX,pypi.org,DIRECT
  - DOMAIN-SUFFIX,docker.com,DIRECT
  
  # CDN 服务
  - DOMAIN-SUFFIX,cloudflare.com,DIRECT
  - DOMAIN-SUFFIX,jsdelivr.net,DIRECT
  - DOMAIN-SUFFIX,unpkg.com,DIRECT
```

---

## ⚠️ 注意事项

### 1. 规则优先级

**白名单规则必须放在最前面**，在广告拦截规则之前：

```yaml
rules:
  # ✅ 正确：白名单在前
  - DOMAIN-SUFFIX,example.com,DIRECT  # 白名单
  - RULE-SET,AWAvenue-Ads-Rule,REJECT # 广告拦截
  
  # ❌ 错误：广告拦截在前
  - RULE-SET,AWAvenue-Ads-Rule,REJECT # 先拦截了
  - DOMAIN-SUFFIX,example.com,DIRECT  # 不会生效
```

### 2. 域名匹配范围

```yaml
# 只匹配 example.com 及其子域名
- DOMAIN-SUFFIX,example.com,DIRECT

# 匹配完整的域名
- DOMAIN,www.example.com,DIRECT

# 匹配包含关键字的域名
- DOMAIN-KEYWORD,example,DIRECT
```

### 3. 性能考虑

- 白名单规则不宜过多，建议只添加确实需要的
- 优先使用 `DOMAIN-SUFFIX`，性能较好
- 定期清理不再需要的白名单规则

---

## 🔧 高级配置

### 按应用分流（Android）

```yaml
rules:
  # 特定应用走直连
  - PROCESS-NAME,com.example.app,DIRECT
  - PROCESS-NAME,com.android.chrome,DIRECT
  
  # 其他应用正常拦截广告
  - RULE-SET,AWAvenue-Ads-Rule,REJECT
```

### 按时间段分流

需要配合 Clash Meta 的定时任务功能：

```yaml
# 工作时间访问特定网站
rules:
  - AND,((DOMAIN-SUFFIX,work.com),(TIME_RANGE,09:00-18:00)),DIRECT
```

### 组合规则

```yaml
rules:
  # 特定应用在特定时间访问特定网站
  - AND,((PROCESS-NAME,com.example.app),(DOMAIN-SUFFIX,example.com)),DIRECT
```

---

## 📖 相关资源

- [Clash Meta 官方文档](https://docs.metacubex.one/)
- [规则语法说明](README.md#规则语法参考)
- [快速配置指南](QUICKSTART.md)

---

## 💡 常见问题

### Q: 添加了白名单为什么不生效？
A: 检查规则是否放在了广告拦截规则之前，规则顺序很重要。

### Q: 如何知道哪些域名被拦截了？
A: 查看 Clash Meta 的日志，筛选 REJECT 级别的记录。

### Q: 白名单太多会影响性能吗？
A: 少量白名单（<100 条）对性能影响很小，可以放心使用。

### Q: 可以临时禁用广告拦截吗？
A: 可以在 Clash Meta 中切换到「Global」模式，选择「DIRECT」。

### Q: 如何分享我的白名单配置？
A: 可以将白名单规则整理成文件，通过 GitHub 分享。

---

**最后更新**: 2026-04-16
