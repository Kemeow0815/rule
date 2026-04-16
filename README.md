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

编辑 `data/config.yaml`，在 `rules` 部分添加：

```yaml
rules:
  # 自定义拦截规则
  - DOMAIN-SUFFIX,example-ad.com,REJECT
  - DOMAIN-KEYWORD,ads,REJECT
  
  # 自定义白名单
  - DOMAIN-SUFFIX,example.com,DIRECT
```

### 修改 DNS 配置

编辑 `data/config.yaml` 中的 `dns` 部分：

```yaml
dns:
  nameserver:
    - https://your-custom-dns.com/dns-query
```

## 注意事项

1. **规则更新**：首次使用可能需要等待几分钟下载规则
2. **网络访问**：部分规则源可能需要代理才能下载
3. **兼容性**：确保使用 Clash Meta 内核（Mihomo）
4. **性能影响**：规则数量较多可能略微增加内存占用

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
