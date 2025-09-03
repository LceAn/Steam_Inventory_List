/*
 * @Author: LceAn 63484787+LceAn@users.noreply.github.com
 * @Date: 2025-09-02 21:35:33
 * @LastEditors: LceAn 63484787+LceAn@users.noreply.github.com
 * @LastEditTime: 2025-09-02 21:35:41
 * @FilePath: /Steam_Inventory_List/控制台.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
// 1. 查找目标元素（class 包含 "_3tY9vKLCmyG2H2Q4rUJpkr" "Panel" "Focusable"）
const targetElement = document.querySelector('._3tY9vKLCmyG2H2Q4rUJpkr.Panel.Focusable');
if (!targetElement) {
  alert('未找到目标元素，请确认游戏列表已加载，或按提示通过元素选择器选中标题后向上级查找');
} else {
  // 2. 复制元素 outerHTML 并处理（原步骤中的去空/格式化逻辑，补充常见空白字符处理）
  let str = targetElement.outerHTML;
  const result = str.replace(/\s+/g, ' ').trim(); // 统一处理多余空格、换行等空白字符
  
  // 3. 输出结果并通过创建文本框实现复制
  console.log('处理后的元素内容：', result);
  // 创建文本域用于复制
  const textarea = document.createElement('textarea');
  textarea.value = result;
  document.body.appendChild(textarea);
  // 选中文本域内容
  textarea.select();
  // 执行复制命令
  try {
    const successful = document.execCommand('copy');
    if (successful) {
      alert('元素内容已复制到剪贴板！\n下一步：在 VSCode 新建 HTML 文件，在 <body> 标签内粘贴即可');
    } else {
      alert('复制失败，请手动选中文本域内容进行复制');
    }
  } catch (err) {
    console.error('复制命令执行失败：', err);
    alert('复制失败，请手动选中文本域内容进行复制');
  }
  // 移除文本域
  document.body.removeChild(textarea);
}