#!/usr/bin/env python3
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find from <!DOCTYPE html> down to <body
body_start = text.find('<body class="bg-slate-950')

clean_pre_body = '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>BayFlow - 이베이 셀러 올인원 자동화 대시보드</title>
  <!-- PWA Meta Tags -->
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#1e293b">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="BayFlow">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
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
  </script>
  <style>
    /* Mobile app scroll & touch behavior */
    body {
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }
    .custom-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .custom-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>
'''

new_text = clean_pre_body + text[body_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Pre-body completely cleaned up!")
