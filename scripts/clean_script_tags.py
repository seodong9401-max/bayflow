#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean up <head> script
# Find from tailwind.config down to </head>
head_start = html.find('  <script src="https://cdn.tailwindcss.com"></script>')
head_end = html.find('</head>')

head_content = html[head_start:head_end]

# Extract everything from `// K-Packet 100x150 라벨 인쇄 모달 제어` to `</script>`
extract_start = head_content.find('    // K-Packet 100x150 라벨 인쇄 모달 제어')
extract_end = head_content.rfind('  </script>')

extracted_code = head_content[extract_start:extract_end]

# Replace inside `triggerPrintKpacket` any `<script>` or `</script>` with split string
extracted_code = extracted_code.replace('<script>', "' + '<sc' + 'ript>' + '")
extracted_code = extracted_code.replace('<\\/script>', "' + '</sc' + 'ript>' + '")
extracted_code = extracted_code.replace('</script>', "' + '</sc' + 'ript>' + '")

# Remove leftover syntax error `);\n    }`
extracted_code = extracted_code.replace(');\n    }\n\n    // 초기 리서치 카테고리 로드', '\n\n    // 초기 리서치 카테고리 로드')
extracted_code = re.sub(r'\);\s*\}\s*\n\s*// 초기 리서치 카테고리 로드', '\n\n    // 초기 리서치 카테고리 로드', extracted_code)

# New clean <head> tailwind script
new_head_script = '''  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#eef2ff',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
            }
          }
        }
      }
    };
  </script>'''

html = html[:head_start] + new_head_script + '\n' + html[head_start + extract_end + 11:]

# 2. Append extracted_code to the main application script right before PWA service worker
target_marker = '    // PWA Service Worker Registration & Force Update'
if target_marker in html:
    html = html.replace(target_marker, extracted_code + '\n\n' + target_marker, 1)
else:
    # Just before last </script>
    last_script_end = html.rfind('  </script>')
    html = html[:last_script_end] + extracted_code + '\n' + html[last_script_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html scripts successfully cleaned and consolidated!")
