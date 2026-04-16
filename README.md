# Clash Meta 去广告规则

本项目提供基于 Clash Meta 的去广告订阅配置，整合多个优质广告规则源，实现智能 DNS 分流，有效拦截广告的同时保证正常网络访问。

## 功能特性

- ✅ **多规则源整合**：整合三个主流去广告规则源，提高广告拦截覆盖率
- ✅ **DNS 智能分流**：国内域名使用去广告 DNS，国外域名使用公共 DNS
- ✅ **自动更新**：每 4 小时自动更新规则，确保规则始终保持最新
- ✅ **兼容性好**：适用于 Clash Meta for Android 及其他 Clash Meta 客户端

## 规则源

本项目整合以下广告规则：

1. **AWAvenue-Ads-Rule**（秋风广告规则）
   - 来源：https://github.com/TG-Twilight/AWAvenue-Ads-Rule
   - 特点：专注于移动端广告拦截

2. **DD-AD**
   - 来源：https://github.com/afwfv/DD-AD
   - 特点：综合型广告拦截规则

3. **217heidai adblockfilters**
   - 来源：https://github.com/217heidai/adblockfilters
   - 特点：针对国内应用的广告拦截规则

## DNS 配置

### 去广告 DNS（国内域名）
- `https://2026.dns1.top/dns-query`
- `https://dns.ipv4dns.com/dns-query`
- `http://dns.trli.club/doh/ad-dns-pro`

### 国外 DNS（国外域名）
- `8.8.8.8`（Google DNS）
- `1.1.1.1`（Cloudflare DNS）

## 使用方法

### 方式一：直接订阅（推荐）

1. 获取订阅链接：
   ```
   https://raw.githubusercontent.com/<你的用户名>/rule/main/data/config.yaml
   ```
   
   > 将 `<你的用户名>` 替换为你的 GitHub 用户名

2. 在 Clash Meta for Android 中：
   - 打开应用 → 配置文件
   - 点击「新建配置」→「订阅」
   - 粘贴上述订阅链接
   - 点击「下载」→「应用」

### 方式二：手动导入

1. 下载配置文件：
   - 从本项目的 `data/config.yaml` 下载配置文件
   
2. 导入到 Clash Meta：
   - 将配置文件复制到手机存储
   - 在 Clash Meta for Android 中选择「导入配置」
   - 选择下载的配置文件

### 方式三：使用 GitHub Pages（可选）

1. 启用 GitHub Pages：
   - 进入仓库 Settings → Pages
   - Source 选择 `Deploy from a branch`
   - Branch 选择 `main`，文件夹选择 `/ (root)`
   - 点击 Save

2. 获取订阅链接：
   ```
   https://<你的用户名>.github.io/rule/data/config.yaml
   ```

## 配置说明

### 规则提供者

配置文件会自动下载并缓存以下规则文件到 `data/rule_providers/` 目录：

- `AWAvenue-Ads-Rule-Clash.yaml` - 秋风广告规则
- `DD-AD.yaml` - DD-AD 规则
- `217heidai-adblock.yaml` - 217heidai 规则

### 更新机制

- **自动更新**：GitHub Actions 每 4 小时自动拉取最新规则
- **手动更新**：在 GitHub 仓库页面点击 Actions → Update Ad Rules → Run workflow
- **客户端更新**：在 Clash Meta 中点击配置文件的刷新按钮

### 代理组说明

- **自动选择**：自动选择延迟最低的节点
- **手动选择**：手动选择代理节点
- **AdBlock**：广告拦截策略（默认 REJECT）

## 自定义配置

### 添加自定义规则

#### 方式一：在配置文件中直接添加规则

编辑 `data/config.yaml`，在 `rules` 部分添加：

```yaml
rules:
  # 自定义拦截规则
  - DOMAIN-SUFFIX,example-ad.com,REJECT
  - DOMAIN-KEYWORD,ads,REJECT
  
  # 自定义白名单
  - DOMAIN-SUFFIX,example.com,DIRECT
```

#### 方式二：添加新的规则提供者

1. **编辑配置文件** `data/config.yaml`，在 `rule-providers` 部分添加：

```yaml
rule-providers:
  # 已有的规则提供者...
  
  # 添加新的规则提供者（示例）
  Your-Custom-Rule:
    type: http          # 类型：http（网络下载）或 file（本地文件）
    behavior: classical # 行为：classical（经典规则）或 ipcidr（IP CIDR 规则）或 domain（域名规则）
    format: yaml        # 格式：yaml 或 text
    path: ./rule_providers/your-custom-rule.yaml  # 保存路径
    url: https://example.com/your-rule.yaml       # 规则文件 URL
    interval: 86400     # 更新间隔（秒），86400 = 24 小时
```

2. **更新 GitHub Actions 工作流** `.github/workflows/update-rules.yml`，添加下载命令：

```yaml
- name: Download rule files
  run: |
    # 已有的下载命令...
    
    # 添加新的规则下载
    echo "Downloading Your-Custom-Rule..."
    curl -sL "https://example.com/your-rule.yaml" \
      -o data/rule_providers/your-custom-rule.yaml || echo "Failed to download"
```

3. **在 rules 部分引用新规则**：

```yaml
rules:
  # 已有的规则...
  - RULE-SET,Your-Custom-Rule,REJECT  # 或 DIRECT、代理组名称
```

#### 方式三：添加本地规则文件

1. 在 `data/rule_providers/` 目录下创建 YAML 文件，例如 `my-rules.yaml`：

```yaml
payload:
  - DOMAIN-SUFFIX,ad-example.com
  - DOMAIN-KEYWORD,tracking
  - DOMAIN,specific-ad-server.com
```

2. 在 `config.yaml` 中配置：

```yaml
rule-providers:
  My-Rules:
    type: file
    behavior: classical
    format: yaml
    path: ./rule_providers/my-rules.yaml

rules:
  - RULE-SET,My-Rules,REJECT
```

### 添加私人 DNS

#### 方式一：修改全局 DNS 配置

编辑 `data/config.yaml` 的 `dns` 部分：

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  
  # 添加/修改 DNS 服务器
  nameserver:
    - https://2026.dns1.top/dns-query        # 去广告 DNS 1
    - https://dns.ipv4dns.com/dns-query      # 去广告 DNS 2
    - http://dns.trli.club/doh/ad-dns-pro    # 去广告 DNS 3
    - https://your-private-dns.com/dns-query # 你的私人 DNS
    - 8.8.8.8                                # Google DNS（备用）
    - 1.1.1.1                                # Cloudflare DNS（备用）
```

#### 方式二：配置 DNS 分流策略

为不同域名配置不同的 DNS 服务器：

```yaml
dns:
  # ... 其他配置 ...
  
  # DNS 分流策略
  nameserver-policy:
    # 国内域名使用特定 DNS
    '+.cn':
      - https://2026.dns1.top/dns-query
      - https://dns.ipv4dns.com/dns-query
    
    # 特定域名使用自定义 DNS
    '+.example.com':
      - https://your-custom-dns.com/dns-query
    
    # 国外域名使用公共 DNS
    '+.google.com':
      - 8.8.8.8
      - 1.1.1.1
    '+.github.com':
      - 8.8.8.8
    '+.youtube.com':
      - 8.8.8.8
```

#### 方式三：使用加密 DNS（DoH/DoT）

Clash Meta 支持多种加密 DNS 协议：

```yaml
dns:
  nameserver:
    # DNS over HTTPS (DoH)
    - https://dns.google/dns-query
    - https://cloudflare-dns.com/dns-query
    - https://dns.adguard-dns.com/dns-query  # AdGuard 去广告 DNS
    
    # DNS over TLS (DoT)
    - tls://dns.google:853
    - tls://one.one.one.one:853
    
    # 传统 UDP DNS
    - 8.8.8.8
    - 1.1.1.1
```

### 常用 DNS 服务器推荐

#### 去广告 DNS

| DNS 提供商 | 地址 | 类型 |
|-----------|------|------|
| AdGuard | `https://dns.adguard-dns.com/dns-query` | DoH |
| 2026.dns1.top | `https://2026.dns1.top/dns-query` | DoH |
| dns.ipv4dns.com | `https://dns.ipv4dns.com/dns-query` | DoH |
| NextDNS | `https://dns.nextdns.io/dns-query` | DoH |

#### 国内 DNS

| DNS 提供商 | 地址 |
|-----------|------|
| 阿里 DNS | `223.5.5.5`、`https://dns.alidns.com/dns-query` |
| 腾讯 DNS | `119.29.29.29`、`https://doh.pub/dns-query` |
| 114 DNS | `114.114.114.114` |

#### 国外 DNS

| DNS 提供商 | 地址 |
|-----------|------|
| Google DNS | `8.8.8.8`、`https://dns.google/dns-query` |
| Cloudflare | `1.1.1.1`、`https://cloudflare-dns.com/dns-query` |
| Quad9 | `9.9.9.9`、`https://dns.quad9.net/dns-query` |

### 规则语法参考

#### Clash 规则类型

```yaml
# 域名完全匹配
- DOMAIN,example.com,REJECT

# 域名后缀匹配
- DOMAIN-SUFFIX,example.com,REJECT

# 域名关键字匹配
- DOMAIN-KEYWORD,ads,REJECT

# IP CIDR 匹配
- IP-CIDR,192.168.1.0/24,DIRECT

# IP CIDR（带源地址）
- IP-CIDR6,::1/128,DIRECT

# 地理位置 IP
- GEOIP,CN,DIRECT

# 规则集（使用 rule-providers）
- RULE-SET,Provider-Name,REJECT

# 进程名匹配
- PROCESS-NAME,Chrome.exe,DIRECT

# 匹配所有
- MATCH,DIRECT
```

#### 规则动作

- `REJECT`：拒绝连接（拦截广告）
- `DIRECT`：直连（不使用代理）
- `代理组名称`：使用指定代理组
- `REJECT-DROP`：直接丢弃（不返回任何信息）

### 完整配置示例

以下是一个添加自定义规则和 DNS 的完整示例：

```yaml
# config.yaml 片段

rule-providers:
  # 已有规则...
  
  # 添加自定义规则
  Block-Tracking:
    type: http
    behavior: classical
    format: yaml
    path: ./rule_providers/block-tracking.yaml
    url: https://raw.githubusercontent.com/example/tracking/main/rules.yaml
    interval: 86400
  
  # 添加白名单规则
  Whitelist:
    type: file
    behavior: classical
    format: yaml
    path: ./rule_providers/whitelist.yaml

dns:
  enable: true
  enhanced-mode: fake-ip
  
  # 主 DNS（去广告）
  nameserver:
    - https://2026.dns1.top/dns-query
    - https://dns.adguard-dns.com/dns-query
  
  # 备用 DNS
  fallback:
    - 8.8.8.8
    - 1.1.1.1
  
  # DNS 分流
  nameserver-policy:
    '+.cn':
      - https://dns.alidns.com/dns-query
    '+.google.com':
      - 8.8.8.8

rules:
  # 白名单优先（必须放在最前面）
  - RULE-SET,Whitelist,DIRECT
  
  # 广告拦截规则
  - RULE-SET,AWAvenue-Ads-Rule,REJECT
  - RULE-SET,DD-AD,REJECT
  - RULE-SET,Block-Tracking,REJECT
  
  # 其他规则...
  - GEOIP,CN,DIRECT
  - MATCH,自动选择
```

### 验证配置

修改配置后，建议先验证 YAML 格式：

```bash
# 使用 Python 验证
python -c "import yaml; yaml.safe_load(open('data/config.yaml', encoding='utf-8'))"
```

或在 Clash Meta 中导入前使用在线 YAML 验证工具检查。

### 注意事项

1. **规则优先级**：rules 列表中的规则**从上到下**依次匹配，第一条匹配的规则生效
2. **白名单处理**：如果需要白名单，请将白名单规则放在广告拦截规则**之前**
3. **DNS 缓存**：修改 DNS 配置后，建议清除 DNS 缓存或重启 Clash Meta
4. **规则数量**：过多的规则会增加内存占用和匹配时间，建议根据需要选择
5. **更新频率**：频繁更新规则可能触发 GitHub API 限制，建议合理设置 interval

## 故障排除

### 规则下载失败

检查网络连接，或尝试手动下载规则文件：

```bash
curl -L "规则 URL" -o data/rule_providers/规则文件.yaml
```

### DNS 解析问题

如果遇到 DNS 解析问题，可以尝试：

1. 切换为其他 DNS 服务器
2. 关闭 DNS 增强模式
3. 重启 Clash Meta 应用

### 广告拦截失效

1. 检查规则是否已下载完成
2. 更新规则到最新版本
3. 清除浏览器缓存和 DNS 缓存

### 配置文件导入失败

1. 检查 YAML 格式是否正确
2. 检查配置文件编码是否为 UTF-8
3. 查看 Clash Meta 日志获取错误信息

## 项目结构

```
rule/
├── .github/
│   └── workflows/
│       └── update-rules.yml    # GitHub Actions 工作流
├── data/
│   ├── config.yaml             # 主配置文件
│   └── rule_providers/         # 规则文件目录（自动生成）
│       ├── AWAvenue-Ads-Rule-Clash.yaml
│       ├── DD-AD.yaml
│       └── 217heidai-adblock.yaml
└── README.md                   # 使用说明
```

## 许可证

本项目仅供学习研究使用。

## 鸣谢

感谢以下规则源的维护者：

- [AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)
- [DD-AD](https://github.com/afwfv/DD-AD)
- [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters)

## 更新日志

- 2026-04-16：初始版本，整合三个广告规则源，实现 DNS 智能分流
