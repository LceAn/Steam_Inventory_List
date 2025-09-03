# Steam_Inventory_List
用于获取steam用户相关的游戏列表

这是一个通过浏览器控制台和Python脚本，将您的Steam游戏库完整信息导出为详细CSV表格文件的工具集。

整个流程分为两步：

1.  **前端抓取**：在浏览器中执行一段JavaScript代码，自动抓取并复制包含所有游戏信息的HTML代码。
2.  **后端处理**：运行一个Python脚本，解析前面抓取的HTML，将其清洗、整理并转换为一个结构化的CSV表格文件。

## ✨ 功能特性

导出的CSV表格信息全面，包含以下中文列名：

  * App ID
  * 游戏名称
  * 游戏时长 (小时)
  * 已解锁成就
  * 总成就数
  * 成就完成度
  * 原始时长文本
  * 商店链接
  * 成就链接
  * 头部图片链接
  * 库图片链接

## 🛠️ 准备工作

在开始之前，请确保您的电脑已安装：

1.  **Python 3**：[Python官网](https://www.python.org/)
2.  **BeautifulSoup4库**：在您的终端或命令提示符中运行以下命令进行安装：
    ```bash
    pip3 install beautifulsoup4
    ```

## 🚀 使用步骤

### 步骤一：获取游戏列表HTML

1.  **打开Steam游戏页面**：
    在浏览器（推荐Chrome或Firefox）中登录您的Steam账户，并访问您的**游戏库页面**。需要登录一个steam账号，否则无法获取游戏列表。

    通常链接格式为：`https://steamcommunity.com/id/你的自定义ID/games/?tab=all` 
    您可以点击 [这里](https://steamcommunity.com/id/aeorz/games/?tab=all) 以访问我的游戏库页面作为示例。
    

2.  **等待页面完全加载**：
    确保您能看到所有的游戏列表都已显示出来。

3.  **运行控制台脚本**：

      * 按 `F12` 键 (或者 Mac上的 `Cmd+Opt+I`) 打开开发者工具，并切换到 **"Console" (控制台)** 选项卡。
      * 将下面的\*\*“控制台.js”**脚本代码**完整复制\*\*并粘贴到控制台中，然后按 `Enter` (回车) 键。


    ```javascript
    // 注意：下面的 class 名 "_3tY9vKLCmyG2H2Q4rUJpkr" 可能会随Steam更新而改变。
    // 如果脚本提示未找到，请使用元素选择器找到包裹所有游戏的那个<div>元素，并替换掉这里的class名。
    const targetElement = document.querySelector('._3tY9vKLCmyG2H2Q4rUJpkr.Panel.Focusable');
    if (!targetElement) {
      alert('未找到目标元素，请确认游戏列表已加载，或按提示通过元素选择器选中标题后向上级查找');
    } else {
      let str = targetElement.outerHTML;
      const result = str; // 直接使用outerHTML，后续由Python处理
      
      const textarea = document.createElement('textarea');
      textarea.value = result;
      document.body.appendChild(textarea);
      textarea.select();
      try {
        const successful = document.execCommand('copy');
        if (successful) {
          alert('游戏列表的HTML内容已成功复制到剪贴板！');
        } else {
          alert('复制失败，请手动从控制台输出中复制。');
        }
      } catch (err) {
        console.error('复制命令执行失败：', err);
        alert('复制失败，请手动从控制台输出中复制。');
      }
      document.body.removeChild(textarea);
    }
    ```

4.  脚本运行成功后，会弹窗提示“游戏列表的HTML内容已成功复制到剪贴板！”。

### 步骤二：创建 `index.html` 文件

1.  在您的项目文件夹中，创建一个新的文件。
2.  将该文件命名为 `index.html`。
3.  打开这个空白文件，将刚才从剪贴板**粘贴**过来的所有内容放进去，然后**保存**文件。

### 步骤三：运行Python脚本进行转换

1.  确保您的项目文件夹中包含以下两个文件：
      * `index.html` (您刚刚创建的)
      * `convert.py` (下面的Python脚本)
2.  在终端中，使用`cd`命令进入该文件夹。
3.  运行转换脚本：
    ```bash
    python3 convert.py
    ```

    ```python
    # 文件名: convert.py
    import csv
    import re
    from bs4 import BeautifulSoup

    # --- 配置 ---
    INPUT_HTML_FILE = 'index.html'
    OUTPUT_CSV_FILE = 'steam_games_full_details_chinese.csv' 

    def parse_game_data(html_content):
        """
        解析HTML，提取所有可用的详细信息，包括链接和图片地址。
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        games_data = []

        # 注意：这里的class名是根据您之前提供的HTML片段定制的，如果HTML结构变化，需要修改这里
        game_rows = soup.find_all('div', class_='_2-pQFn1G7dZ7667rrakcU3')

        if not game_rows:
            print("❌ 错误: 未能在HTML文件中找到任何游戏条目。请检查JS脚本抓取的内容是否正确。")
            return []

        print(f"✅ 找到 {len(game_rows)} 个游戏条目，正在进行全量信息提取...")

        for row in game_rows:
            try:
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
                
                header_image_url = find_attr('img', '', 'src')
                library_image_url = find_attr('source', '', 'srcset')

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
            writer = csv.DictWriter(csvfile, fieldnames=headers.keys())
            writer.writerow(headers)
            writer.writerows(data)

        print(f"\n🎉 完美！您的全量数据已保存到 '{filename}'。")

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
    ```


### 步骤四：完成！

脚本运行成功后，您的文件夹中会出现一个名为 `steam_games_full_details_chinese.csv` 的文件。您可以使用Microsoft Excel, Google Sheets, Apple Numbers等任意表格软件打开它，查看您已导出的完整游戏库信息。