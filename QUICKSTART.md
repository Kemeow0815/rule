# 快速配置指南

## 问题已修复 ✅

配置文件已更新，添加了 `proxy-providers` 部分以解决以下错误：

```
add profile error: profile does not contain `proxies` or `proxy-providers`
```

## 使用场景

### 场景 1：仅去广告，不使用代理

直接导入配置文件即可，无需额外配置。

**适用情况**：
- 只需要去广告功能
- 国内网络环境，不需要访问国外网站
- Clash Meta 仅用作广告拦截器

**配置特点**：
- 已包含空的 `proxy-providers` 部分
- 所有流量默认直连（通过 GEOIP,CN,DIRECT）
- 广告自动拦截

### 场景 2：去广告 + 代理订阅

如果你想同时使用代理订阅，有两种方式：

#### 方式 A：使用代理提供者（推荐）

编辑 `data/config.yaml`，在 `proxy-providers` 部分添加：

```yaml
proxy-providers:
  My-Sub:
    type: http
    url: "https://你的订阅链接.com/sub"
    path: ./proxies/my-sub.yaml
    interval: 3600
    health-check:
      enable: true
      url: http://www.gstatic.com/generate_204
      interval: 300
```

然后修改代理组配置：

```yaml
proxy-groups:
  - name: 自动选择
    type: url-test
    proxies:
      - My-Sub  # 引用代理提供者
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50
  
  - name: 手动选择
    type: select
    proxies:
      - 自动选择
      - DIRECT
```

#### 方式 B：手动添加代理节点

编辑 `data/config.yaml`，添加 `proxies` 部分：

```yaml
proxies:
  - name: "节点 1"
    type: vmess
    server: example.com
    port: 443
    uuid: your-uuid
    alterId: 0
    cipher: auto
    tls: true
  
  - name: "节点 2"
    type: trojan
    server: example2.com
    port: 443
    password: your-password
```

然后修改代理组配置：

```yaml
proxy-groups:
  - name: 自动选择
    type: url-test
    proxies:
      - 节点 1
      - 节点 2
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50
```

### 场景 3：混合模式（本地代理 + 远程订阅）

同时使用本地代理和远程订阅：

```yaml
proxies:
  - name: "本地节点"
    type: vmess
    server: example.com
    port: 443
    uuid: your-uuid

proxy-providers:
  Remote-Sub:
    type: http
    url: "https://你的订阅链接.com/sub"
    path: ./proxies/remote.yaml
    interval: 3600

proxy-groups:
  - name: 全部节点
    type: select
    proxies:
      - 本地节点
      - Remote-Sub
```

## 配置代理组

Clash Meta 支持多种代理组类型：

### 1. 手动选择（select）

```yaml
- name: 手动选择
  type: select
  proxies:
    - 节点 1
    - 节点 2
    - DIRECT
```

### 2. 自动测试（url-test）

自动选择延迟最低的节点：

```yaml
- name: 自动选择
  type: url-test
  proxies:
    - 节点 1
    - 节点 2
  url: http://www.gstatic.com/generate_204
  interval: 300
  tolerance: 50
```

### 3. 故障转移（fallback）

主节点失败时自动切换：

```yaml
- name: 故障转移
  type: fallback
  proxies:
    - 主节点
    - 备用节点 1
    - 备用节点 2
  url: http://www.gstatic.com/generate_204
  interval: 300
```

### 4. 负载均衡（load-balance）

在多个节点间负载均衡：

```yaml
- name: 负载均衡
  type: load-balance
  proxies:
    - 节点 1
    - 节点 2
    - 节点 3
  strategy: round-robin
```

## 规则路由配置

### 代理特定网站

```yaml
rules:
  # 走代理的网站
  - DOMAIN-SUFFIX,google.com,自动选择
  - DOMAIN-SUFFIX,youtube.com,自动选择
  - DOMAIN-SUFFIX,github.com,自动选择
  
  # 国内网站直连
  - GEOIP,CN,DIRECT
  
  # 其他流量
  - MATCH,自动选择
```

### 按应用分流（仅 Android）

```yaml
rules:
  # 特定应用走代理
  - PROCESS-NAME,com.android.chrome,自动选择
  - PROCESS-NAME,com.google.android.youtube,自动选择
  
  # 其他应用直连
  - MATCH,DIRECT
```

## 完整配置示例

```yaml
# 基础配置
mixed-port: 7890
allow-lan: false
mode: rule
log-level: info

# DNS 配置
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  nameserver:
    - https://2026.dns1.top/dns-query
    - https://dns.adguard-dns.com/dns-query
  fallback:
    - 8.8.8.8
    - 1.1.1.1

# 代理提供者
proxy-providers:
  My-Sub:
    type: http
    url: "https://你的订阅链接.com/sub"
    path: ./proxies/my-sub.yaml
    interval: 3600
    health-check:
      enable: true
      url: http://www.gstatic.com/generate_204
      interval: 300

# 规则提供者
rule-providers:
  AWAvenue-Ads-Rule:
    type: http
    behavior: classical
    format: yaml
    path: ./rule_providers/AWAvenue-Ads-Rule-Clash.yaml
    url: https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml
    interval: 86400

# 代理组
proxy-groups:
  - name: 节点选择
    type: select
    proxies:
      - My-Sub
      - DIRECT
  
  - name: 自动选择
    type: url-test
    proxies:
      - My-Sub
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50

# 规则
rules:
  # 广告拦截
  - RULE-SET,AWAvenue-Ads-Rule,REJECT
  
  # 国内直连
  - GEOIP,CN,DIRECT
  
  # 国外网站代理
  - DOMAIN-SUFFIX,google.com,节点选择
  - DOMAIN-SUFFIX,youtube.com,节点选择
  
  # 默认
  - MATCH,节点选择
```

## 验证配置

修改配置后，使用以下命令验证：

```bash
# Windows PowerShell
python -c "import yaml; yaml.safe_load(open('data/config.yaml', encoding='utf-8'))"

# Linux/Mac
python3 -c "import yaml; yaml.safe_load(open('data/config.yaml'))"
```

无错误输出则配置正确。

## 常见问题

### Q: 导入配置后提示错误？
A: 确保配置包含 `proxy-providers` 或 `proxies` 部分。

### Q: 如何使用多个代理订阅？
A: 在 `proxy-providers` 中添加多个提供者，每个使用不同的名称。

### Q: 代理节点不显示？
A: 检查订阅链接是否正确，或手动下载规则文件查看。

### Q: 如何测试节点速度？
A: 使用 `url-test` 类型的代理组，Clash 会自动测试并选择最快节点。

## 相关资源

- [Clash Meta 官方文档](https://docs.metacubex.one/)
- [Clash 配置教程](https://lancellc.gitbook.io/clash)
- [本项目主文档](README.md)
