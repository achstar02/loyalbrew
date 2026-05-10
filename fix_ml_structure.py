import re

# 读取备份文件
with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js.bak', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)}")

# 1. 找到 MERCHANT_LANGS 的开始位置
ml_start = content.find('const MERCHANT_LANGS = {')
print(f"MERCHANT_LANGS 开始位置: {ml_start}")

# 2. 找到目前错误的结束位置
def find_matching_brace(s, start_open_brace):
    depth = 0
    for i in range(start_open_brace, len(s)):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return i
    return -1

obj_start = ml_start + 25
obj_end = find_matching_brace(content, obj_start)
print(f"当前对象体结束位置（错误）: {obj_end}")
print(f"结束符: {repr(content[obj_end:obj_end+2])}")

# 3. 找到 en 块
en_start = content.find('en:', ml_start)
en_brace_start = content.find('{', en_start)
en_end = find_matching_brace(content, en_brace_start)
en_block = content[en_start:en_end+1]
print(f"en 块: {en_start} - {en_end}, 长度: {len(en_block)}")

# 4. 找到 ms 块
ms_start = content.find('ms:', en_end)
ms_brace_start = content.find('{', ms_start)
ms_end = find_matching_brace(content, ms_brace_start)
ms_block = content[ms_start:ms_end+1]
print(f"ms 块: {ms_start} - {ms_end}, 长度: {len(ms_block)}")

# 5. 找到游离的 zh 和 ta 块
zh_start = content.find('\n  zh: {', ml_start)
ta_start = content.find('\n    ta: {', ml_start)

zh_brace_start = content.find('{', zh_start)
zh_end = find_matching_brace(content, zh_brace_start)
zh_block = content[zh_start:zh_end+1]
print(f"zh 块: {zh_start} - {zh_end}, 长度: {len(zh_block)}")

ta_brace_start = content.find('{', ta_start)
ta_end = find_matching_brace(content, ta_brace_start)
ta_block = content[ta_start:ta_end+1]
print(f"ta 块: {ta_start} - {ta_end}, 长度: {len(ta_block)}")

# 6. 组装新的 MERCHANT_LANGS 对象
# 调整缩进：zh 和 ta 需要 2 空格缩进
zh_block_fixed = zh_block.replace('\n    ', '\n  ')  # 4空格 -> 2空格
ta_block_fixed = ta_block.replace('\n        ', '\n  ')  # 8空格 -> 2空格（可能需要多次替换，先简单处理）

new_ml_content = 'const MERCHANT_LANGS = {\n  ' + en_block + ',\n  ' + ms_block + ',\n  ' + zh_block + ',\n  ' + ta_block + '\n};'

# 7. 替换旧内容
old_ml_content = content[ml_start:obj_end+2]
new_content = content[:ml_start] + new_ml_content + content[obj_end+2:]

print(f"旧对象长度: {len(old_ml_content)}")
print(f"新对象长度: {len(new_ml_content)}")

# 8. 写入文件
with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("修复完成！正在验证语法...")

# 9. 验证语法
import subprocess, sys
result = subprocess.run(['node', '-e', 'const fs=require("fs"); try { new Function(fs.readFileSync("C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js", "utf8")); console.log("SYNTAX OK") } catch(e) { console.log("ERROR: " + e.message); process.exit(1) }'], 
                        capture_output=True, text=True, timeout=15)
print("STDOUT:", result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("修复脚本执行完成")
