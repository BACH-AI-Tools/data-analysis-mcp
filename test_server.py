#!/usr/bin/env python3
"""
测试 MCP 服务器的脚本
"""

import httpx
import json
import asyncio


async def test_mcp_server():
    """测试 MCP 服务器的各个功能"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("MCP 服务器测�?)
    print("=" * 60)
    
    # 测试 1: 检查服务器是否运行
    print("\n[测试 1] 检查服务器状�?..")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/")
            print(f"�?服务器运行正�?)
            print(f"  响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"�?服务器未运行: {e}")
        print("  请先启动服务�? python main.py")
        return
    
    # 测试 2: 初始化请�?
    print("\n[测试 2] 发送初始化请求...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/messages",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {}
                }
            )
            result = response.json()
            print(f"�?初始化成�?)
            print(f"  协议版本: {result.get('result', {}).get('protocolVersion')}")
            print(f"  服务器信�? {json.dumps(result.get('result', {}).get('serverInfo'), ensure_ascii=False)}")
    except Exception as e:
        print(f"�?初始化失�? {e}")
    
    # 测试 3: 列出工具
    print("\n[测试 3] 列出可用工具...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/messages",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                }
            )
            result = response.json()
            tools = result.get('result', {}).get('tools', [])
            print(f"�?工具列表获取成功")
            print(f"  共有 {len(tools)} 个工�?")
            for tool in tools:
                print(f"    - {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"�?获取工具列表失败: {e}")
    
    # 测试 4: 调用 list_datasets 工具
    print("\n[测试 4] 调用 list_datasets 工具...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/messages",
                json={
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "list_datasets",
                        "arguments": {}
                    }
                }
            )
            result = response.json()
            content = result.get('result', {}).get('content', [])
            if content:
                print(f"�?工具调用成功")
                print(f"  返回内容: {content[0].get('text')}")
            else:
                print(f"�?工具调用返回为空")
                print(f"  响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"�?工具调用失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成�?)
    print("=" * 60)


async def test_sse_connection():
    """测试 SSE 连接"""
    print("\n[额外测试] 测试 SSE 连接...")
    print("提示: 这将保持连接 5 秒钟...")
    
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', 'http://localhost:8000/sse') as response:
                print(f"�?SSE 连接建立成功 (状态码: {response.status_code})")
                
                count = 0
                async for line in response.aiter_lines():
                    if line:
                        print(f"  收到: {line}")
                        count += 1
                        if count >= 5:  # 只读取前5个事�?
                            break
    except Exception as e:
        print(f"�?SSE 连接失败: {e}")


if __name__ == "__main__":
    print("\n开始测�?MCP 服务�?..")
    print("确保服务器已启动: python main.py\n")
    
    asyncio.run(test_mcp_server())
    asyncio.run(test_sse_connection())

