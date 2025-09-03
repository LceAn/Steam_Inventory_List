#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import requests
import argparse

def get_games_list(profile_url: str):
    """
    从一个公开的Steam个人资料URL中获取并解析游戏列表。
    """
    # 1. 构造完整的“所有游戏”页面URL
    if not profile_url.endswith('/'):
        profile_url += '/'
    games_url = profile_url + "games/?tab=all"
    
    print(f"🔗 正在从以下地址获取游戏列表: {games_url}")

    # 2. 伪装成浏览器发送网络请求
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        response = requests.get(games_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取URL时发生错误: {e}")
        return None

    # --- 这里是关键的修订部分 ---
    # 旧的、已失效的正则表达式
    # match = re.search(r"var g_rgGames\s*=\s*(\[.*\]);", response.text)
    
    # 新的、有效的正则表达式，用于匹配Steam新的数据结构
    match = re.search(r"oGamesListPage\.SetGames\(\s*(\[.*\])\s*\);", response.text)
    
    if not match:
        print("❌ 错误: 未能在页面上找到游戏数据。")
        print("请确认您的个人资料是公开的，并且URL正确无误。这也有可能是Steam再次更新了页面代码。")
        return None
        
    # 4. 解析JSON数据
    try:
        # group(1) 获取的是正则表达式中第一个括号 () 里的内容
        games_data = json.loads(match.group(1))
    except json.JSONDecodeError:
        print("❌ 错误: 解析游戏数据失败。")
        return None

    # 5. 提取我们需要的信息并排序
    game_list = []
    for game in games_data:
        game_list.append({
            'name': game.get('name'),
            'hours': float(game.get('hours_forever', 0)),
            'appid': game.get('appid')
        })
        
    game_list.sort(key=lambda g: g['hours'], reverse=True)
    
    return game_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从一个公开的Steam社区个人资料中获取游戏列表。")
    parser.add_argument("profile_url", help="完整的Steam个人资料URL (例如: https://steamcommunity.com/id/your_id/)")
    args = parser.parse_args()

    games = get_games_list(args.profile_url)
    
    if games:
        print("\n--- 🎮 Steam 游戏库 ---")
        for game in games:
            print(f"{game['name']:<50} | 游戏时长: {game['hours']:>7.2f} 小时")
        print(f"\n✅ 成功找到 {len(games)} 款游戏。")