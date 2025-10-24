"""
AI Research Multi Agent - Google ADK版
"""

import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

# プロジェクトルートをパスに追加
project_root = os.path.join(os.path.dirname(__file__), '../../..')
sys.path.append(project_root)

# プロジェクトルートに移動してから設定を読み込み
os.chdir(project_root)

# 環境変数の設定（.env ファイルがある場合）
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters

# 設定ファイルとプロンプトマネージャー、MCPマネージャーをインポート
from src.config import settings
from src.utils.prompt_manager import PromptManager
from src.utils.mcp_manager import MCPServerManager
from src.client.github_client import GitHubClient

logger = logging.getLogger(__name__)

# MCPServerManager を使用してMCP ツールの設定
mcp_tools = []

# 設定ファイルに基づいてMCP サーバーを設定
if settings.enabled_mcp_servers:
    try:
        # MCPServerManager を初期化
        mcp_manager = MCPServerManager(config_path="mcp/mcp_servers.yaml")
        
        # 有効なMCPサーバーのリストを取得
        enabled_servers_list = [s.strip() for s in settings.enabled_mcp_servers.split(",")]
        
        # 有効なMCPサーバーの設定を取得
        enabled_servers_config = mcp_manager.get_enabled_servers(enabled_servers_list)
        
        # 各MCPサーバーの設定を構築
        for server_name, server_config in enabled_servers_config.items():
            try:
                # 環境変数を展開
                env = {}
                if "env" in server_config:
                    for key, value in server_config["env"].items():
                        # ${VAR_NAME} 形式の環境変数を展開
                        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                            var_name = value[2:-1]
                            env[key] = os.getenv(var_name, "")
                        else:
                            env[key] = value
                
                # stdio タイプのMCPサーバーの場合
                if server_config.get("type") == "stdio":
                    # ドキュメントに基づく正しい StdioConnectionParams の作成
                    connection_params = StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command=server_config.get("command", "npx"), 
                            args=server_config.get("args", []), 
                            env=env
                        )
                    )

                    # MCPToolset を初期化（ドキュメントに基づく正しい方法）
                    mcp_tool = MCPToolset(connection_params=connection_params)
                    mcp_tools.append(mcp_tool)
                    print(f"{server_name} MCP Server を設定しました")
                else:
                    print(f"未対応のMCPサーバータイプ: {server_config.get('type')} (サーバー: {server_name})")
                    
            except Exception as e:
                print(f"{server_name} MCP Server の設定に失敗: {e}")
                
    except Exception as e:
        print(f"MCPServerManager の初期化に失敗: {e}")
        # フォールバック: 従来の方法でGitHub MCP Serverを設定
        enabled_servers = [s.strip() for s in settings.enabled_mcp_servers.split(",")]
        for server_name in enabled_servers:
            if server_name.lower() == "github":
                try:
                    # フォールバック用の GitHub MCP Server 設定
                    connection_params = StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command='npx',
                            args=['-y', '@github/github-mcp-server'],
                            env={'GITHUB_TOKEN': settings.github_token}
                        )
                    )
                    github_mcp_tool = MCPToolset(connection_params=connection_params)
                    mcp_tools.append(github_mcp_tool)
                    print(f"GitHub MCP Server を設定しました (フォールバック)")
                except Exception as e:
                    print(f"GitHub MCP Server の設定に失敗 (フォールバック): {e}")
            else:
                print(f"未対応のMCPサーバー: {server_name}")

# PromptManager を使用してプロンプトを取得
def get_instruction_from_prompt_manager():
    """PromptManager を使用してプロンプトを取得して instruction として設定"""
    try:
        # PromptManager を初期化
        prompt_manager = PromptManager(prompts_dir="prompts")
        
        # 有効なMCPサーバーを取得
        enabled_mcp_servers = [s.strip() for s in settings.enabled_mcp_servers.split(",")] if settings.enabled_mcp_servers else []
        
        # report プロンプトを取得
        instruction = prompt_manager.get_prompt(
            prompt_type="report",
            enabled_mcp_servers=enabled_mcp_servers,
            news_count=str(settings.news_count),
            period="週間"
        )
        
        if instruction:
            return instruction
        else:
            # フォールバック: 基本的な instruction
            return 'あなたはAI技術動向と論文の統合分析を行うエージェントです。最新のAI技術動向を調査し、実用的なアクションプランを提案してください。'
    
    except Exception as e:
        print(f"PromptManager からのプロンプト取得に失敗: {e}")
        # フォールバック: 基本的な instruction
        return 'あなたはAI技術動向と論文の統合分析を行うエージェントです。最新のAI技術動向を調査し、実用的なアクションプランを提案してください。'

# 設定ファイルに基づいてエージェントを作成
instruction = get_instruction_from_prompt_manager()

root_agent = Agent(
    model=settings.model_name,
    name='ai_research_agent',
    description='AI技術動向と論文の統合分析エージェント',
    instruction=instruction,
    tools=mcp_tools if mcp_tools else [],
)

print(f"エージェント設定:")
print(f"  モデル: {settings.model_name}")
print(f"  有効なMCPサーバー: {settings.enabled_mcp_servers}")
print(f"  GitHubリポジトリ: {settings.github_repo}")
print(f"  ニュース件数: {settings.news_count}")
print(f"  MCPサーバー: {mcp_tools}")
print(f"  プロンプト: {instruction}")