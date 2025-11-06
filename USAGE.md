# 使用指南

## 问题修复说明

之前工具获取不到的问题已经修复！现在服务器完全兼容 MCP SSE 协议。

### 主要改进

1. **正确的 SSE 实现**: 现在 SSE 端点会发送 `endpoint` 事件，告诉客户端消息发送地址
2. **会话管理**: 每个 SSE 连接有独立的 session ID
3. **双向通信**: 客户端通过 POST 发送，服务器通过 SSE 返回响应
4. **CORS 支持**: 添加了跨域支持，可以从浏览器访问

## 快速开始

### 1. 启动服务器

```bash
python main.py
```

你会看到：
```
🚀 启动 Data Analysis MCP Server (SSE 模式)
📡 SSE Endpoint: http://localhost:3000/sse
📨 Messages Endpoint: http://localhost:3000/messages
📖 API Docs: http://localhost:3000/docs
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

### 2. 测试服务器

```bash
python test_server.py
```

### 3. 配置 Claude Desktop

#### Windows
编辑文件：`%APPDATA%\Claude\claude_desktop_config.json`

#### macOS  
编辑文件：`~/Library/Application Support/Claude/claude_desktop_config.json`

#### 配置内容
```json
{
  "mcpServers": {
    "data-analysis": {
      "url": "http://localhost:3000/sse",
      "transport": "sse"
    }
  }
}
```

### 4. 重启 Claude Desktop

配置完成后，重启 Claude Desktop。

## 验证连接

在 Claude Desktop 中，你可以这样测试：

```
请列出数据分析相关的工具
```

你应该看到 5 个工具：
- `load_data` - 加载数据文件
- `describe_data` - 获取数据统计
- `analyze_column` - 分析特定列
- `correlation_analysis` - 相关性分析
- `list_datasets` - 列出已加载数据集

## 使用示例

### 示例 1: 加载并分析 CSV 文件

```
我有一个名为 sales.csv 的文件，请帮我：
1. 加载这个文件（命名为 sales）
2. 查看数据的统计摘要
3. 分析 revenue 列
```

### 示例 2: 相关性分析

```
请对 sales 数据集进行相关性分析，找出哪些列之间有强相关性
```

## API 端点说明

### GET /
返回服务器信息

### GET /sse
SSE 连接端点，客户端应该连接到这里接收服务器消息

### POST /message
发送 MCP 消息的端点（带 sessionId 参数时通过 SSE 返回）

### POST /messages  
兼容端点，直接返回 JSON 响应

## 手动测试 API

### 使用 curl

```bash
# 列出工具
curl -X POST http://localhost:3000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'

# 列出数据集
curl -X POST http://localhost:3000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "list_datasets",
      "arguments": {}
    }
  }'
```

### 使用 Python

```python
import httpx
import json

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:3000/messages",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
    )
    print(json.dumps(response.json(), indent=2))
```

## 故障排除

### 工具列表为空？
- 检查服务器日志中是否有错误
- 运行 `python test_server.py` 验证服务器功能
- 确保使用的是正确的端点 URL

### Claude Desktop 无法连接？
1. 确认服务器正在运行
2. 检查配置文件路径是否正确
3. 验证 JSON 格式是否正确
4. 重启 Claude Desktop

### 端口冲突？
修改 `main.py` 中的端口号：
```python
uvicorn.run(app, host="0.0.0.0", port=3000)  # 改为其他端口
```

同时更新配置中的 URL。

## 支持的数据格式

- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`) 
- JSON (`.json`)

## 下一步

- 查看 `README.md` 了解详细功能
- 查看 `CONFIG_GUIDE.md` 了解配置细节
- 访问 http://localhost:3000/docs 查看 API 文档

