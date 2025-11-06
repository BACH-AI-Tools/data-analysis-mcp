# MCP 配置指南

## Claude Desktop 配置

### Windows 配置路径

编辑文件：`%APPDATA%\Claude\claude_desktop_config.json`

完整路径示例�?
```
C:\Users\你的用户名\AppData\Roaming\Claude\claude_desktop_config.json
```

### macOS 配置路径

编辑文件：`~/Library/Application Support/Claude/claude_desktop_config.json`

### 配置内容

将以下内容添加到配置文件中：

```json
{
  "mcpServers": {
    "data-analysis": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

如果已有其他 MCP 服务器配置，请将 `data-analysis` 部分添加到现有的 `mcpServers` 对象中：

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "node",
      "args": ["path/to/server.js"]
    },
    "data-analysis": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

## 使用步骤

### 1. 启动 MCP 服务�?

在项目目录下运行�?

```bash
python main.py
```

你应该看到类似的输出�?
```
🚀 启动 Data Analysis MCP Server (SSE 模式)
📡 SSE Endpoint: http://localhost:8000/sse
📨 Messages Endpoint: http://localhost:8000/messages
📖 API Docs: http://localhost:8000/docs
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. 配置 Claude Desktop

1. 找到并编�?`claude_desktop_config.json` 文件
2. 添加上述配置内容
3. 保存文件
4. 重启 Claude Desktop

### 3. 验证连接

�?Claude Desktop 中，你应该能看到 "data-analysis" 服务器已连接�?

你可以向 Claude 发送类似的请求�?
- "请列出可用的数据分析工具"
- "帮我加载 data.csv 文件"
- "分析这个数据集的统计信息"

## 手动测试 API

### 测试根端�?

```bash
curl http://localhost:8000/
```

### 测试 SSE 连接

```bash
curl http://localhost:8000/sse
```

### 测试消息端点

```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

### 使用 httpx (Python)

```python
import httpx
import json

# 测试列出工具
response = httpx.post(
    "http://localhost:8000/messages",
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
)
print(json.dumps(response.json(), indent=2))
```

## 故障排除

### 服务器无法启�?

- **端口被占�?*：修�?`main.py` 中的端口号（默认 8000�?
- **缺少依赖**：运�?`pip install -r requirements.txt`

### Claude Desktop 无法连接

1. 确认服务器正在运�?
2. 检查防火墙设置
3. 验证配置文件路径和格�?
4. 重启 Claude Desktop

### 工具调用失败

- 检查服务器日志中的错误信息
- 验证文件路径是否正确
- 确保数据文件格式受支持（CSV、Excel、JSON�?

## 高级配置

### 修改服务器端�?

编辑 `main.py` 文件的最后几行：

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,  # 修改此端口号
    log_level="info"
)
```

同时更新配置文件中的 URL�?

```json
{
  "mcpServers": {
    "data-analysis": {
      "url": "http://localhost:新端口号/sse",
      "transport": "sse"
    }
  }
}
```

### 远程访问

如果需要从其他机器访问，修改配置中�?`localhost` 为服务器 IP 地址�?

```json
{
  "mcpServers": {
    "data-analysis": {
      "url": "http://192.168.1.100:8000/sse",
      "transport": "sse"
    }
  }
}
```

**注意**：确保防火墙允许访问该端口�?

## 安全建议

- 不要在公网环境下直接暴露服务�?
- 考虑添加身份验证机制
- 使用 HTTPS（需要配�?SSL 证书�?
- 限制允许访问�?IP 地址范围

