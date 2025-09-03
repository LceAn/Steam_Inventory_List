import csv
import re
from bs4 import BeautifulSoup

# --- 配置 ---
INPUT_HTML_FILE = 'index.html'
OUTPUT_CSV_FILE = 'steam_games_full_details_chinese.csv' # 新文件名，防止覆盖

def parse_game_data(html_content):
    """
    解析HTML，提取所有可用的详细信息，包括链接和图片地址。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    games_data = []

    game_rows = soup.find_all('div', class_='_2-pQFn1G7dZ7667rrakcU3')

    if not game_rows:
        print("❌ 错误: 未能找到任何游戏条目。请检查HTML文件结构。")
        return []

    print(f"✅ 找到 {len(game_rows)} 个游戏条目，正在进行全量信息提取...")

    for row in game_rows:
        try:
            # 使用 .get() 和三元运算符来优雅地处理可能不存在的元素
            # 定义一个辅助函数来简化查找过程
            def find_text(tag, class_name):
                element = row.find(tag, class_=class_name)
                return element.text.strip() if element else 'N/A'

            def find_attr(tag, class_name, attr):
                element = row.find(tag, class_=class_name)
                return element.get(attr, 'N/A') if element else 'N/A'

            # 提取数据
            name = find_text('a', '_22awlPiAoaZjQMqxJhp-KP')
            
            full_playtime_text = find_text('span', '_26nl3MClDebGDV7duYjZVn')
            match_hours = re.search(r'[\d,]+\.?\d*', full_playtime_text.replace(',', ''))
            hours = float(match_hours.group(0)) if match_hours else 0.0

            achievement_text = find_text('span', '_1YRRMk6X7vrOL-02K-q1pf')
            achievements_unlocked, achievements_total = ('0', '0')
            if '/' in achievement_text:
                achievements_unlocked, achievements_total = achievement_text.split('/')

            store_link = find_attr('a', '_1bAC6eBHy0MpRWrwTkgT9o', 'href')
            app_id = re.search(r'/app/(\d+)', store_link).group(1) if '/app/' in store_link else 'N/A'

            achievement_link = find_attr('a', '_3eZMLQT-bjZ0EhBSvQlDQ0', 'href')
            
            header_image_url = find_attr('img', '', 'src') # img标签没有特定class
            library_image_url = find_attr('source', '', 'srcset') # source标签没有特定class

            # 提取成就完成度百分比
            percent_div = row.find('div', class_='_3szjUMH5QeRwtXAsLRcWt9')
            achievement_percent = '0.0'
            if percent_div and percent_div.get('style'):
                style_text = percent_div['style']
                match_percent = re.search(r'--percent:\s*([\d\.]+)', style_text)
                if match_percent:
                    achievement_percent = match_percent.group(1)
            
            games_data.append({
                'app_id': app_id,
                'title': name,
                'hours': hours,
                'full_playtime_text': full_playtime_text,
                'achievements_unlocked': achievements_unlocked,
                'achievements_total': achievements_total,
                'achievement_percent': achievement_percent,
                'store_link': store_link,
                'achievement_link': achievement_link,
                'header_image_url': header_image_url,
                'library_image_url': library_image_url,
            })
        except Exception as e:
            print(f"⚠️ 警告: 解析某个游戏条目时出错，已跳过。错误: {e}")

    return games_data

def save_to_csv(data, filename):
    """将全量数据使用中文表头保存到CSV文件。"""
    if not data:
        print("没有可供保存的数据。")
        return

    data.sort(key=lambda x: x['hours'], reverse=True)

    # 英文键名 -> 中文表头 的映射
    headers = {
        'app_id': 'App ID',
        'title': '游戏名称',
        'hours': '游戏时长 (小时)',
        'achievements_unlocked': '已解锁成就',
        'achievements_total': '总成就数',
        'achievement_percent': '成就完成度',
        'full_playtime_text': '原始时长文本',
        'store_link': '商店链接',
        'achievement_link': '成就链接',
        'header_image_url': '头部图片链接',
        'library_image_url': '库图片链接',
    }

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # 使用headers.keys()作为fieldnames来匹配字典，使用headers.values()作为要写入的表头
        writer = csv.DictWriter(csvfile, fieldnames=headers.keys())
        
        # 写入中文表头
        writer.writerow(headers)
        
        # 写入数据行
        writer.writerows(data)

    print(f"\n🎉 完美！您的全量数据已保存到 '{filename}'。")
    print("表格已包含所有提取的信息，并使用了中文列名。")

def main():
    try:
        with open(INPUT_HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ 错误: 输入文件 '{INPUT_HTML_FILE}' 未找到。")
        return
    
    parsed_data = parse_game_data(html_content)
    save_to_csv(parsed_data, OUTPUT_CSV_FILE)

if __name__ == '__main__':
    main()