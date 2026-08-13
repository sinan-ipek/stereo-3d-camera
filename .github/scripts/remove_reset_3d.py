from pathlib import Path
import re

project = Path('StereoGuide')
res = project / 'app/src/main/res'

# 1) Görünen etiketleri doğrudan layout'a yaz.
# Böylece eski cm metinleri veya kaynak önbelleği hiçbir şekilde ekrana gelemez.
layout_path = res / 'layout/activity_main.xml'
layout = layout_path.read_text(encoding='utf-8')

label_replacements = {
    'android:text="@string/close_4cm"': 'android:text="Yakın"',
    'android:text="@string/portrait_6cm"': 'android:text="Portre"',
    'android:text="@string/landscape_8cm"': 'android:text="Uzak"',
    'android:text="@string/macro_12cm"': 'android:text="Hiper"',
    'android:text="@string/zoom_wide"': 'android:text="0.6×"',
    'android:text="@string/zoom_normal"': 'android:text="1×"',
}
for old, new in label_replacements.items():
    layout = layout.replace(old, new)

# Zoom düğmelerine biraz daha alan ver; 0.6× hiçbir zaman kesilmesin.
layout = layout.replace('android:layout_width="64dp"\n            android:layout_height="42dp"',
                        'android:layout_width="76dp"\n            android:layout_height="42dp"')

# Mod düğmelerini birbirinden hafif ayır; kabartı/gölge görünür olsun.
for view_id in ('close', 'portrait', 'landscape', 'macro'):
    marker = f'android:id="@+id/{view_id}"'
    if marker in layout and f'{marker}\n                android:layout_marginHorizontal="2dp"' not in layout:
        layout = layout.replace(marker, marker + '\n                android:layout_marginHorizontal="2dp"')

# 2) Sıfırla / yeniden dene düğmesini arayüzden tamamen kaldır.
reset_marker = 'android:id="@+id/reset"'
idx = layout.find(reset_marker)
if idx != -1:
    start = layout.rfind('<com.google.android.material.button.MaterialButton', 0, idx)
    end = layout.find('/>', idx)
    if start == -1 or end == -1:
        raise RuntimeError('Reset düğmesi XML bloğu bulunamadı.')
    layout = layout[:start] + layout[end + 2:]
if reset_marker in layout:
    raise RuntimeError('Reset düğmesi arayüzden tamamen kaldırılamadı.')

# Toggle gruplarında gölge/yükselme kesilmesin.
if 'android:id="@+id/zoomGroup"\n        android:clipChildren="false"' not in layout:
    layout = layout.replace(
        'android:id="@+id/zoomGroup"',
        'android:id="@+id/zoomGroup"\n        android:clipChildren="false"\n        android:clipToPadding="false"',
    )
if 'android:id="@+id/distanceGroup"\n            android:clipChildren="false"' not in layout:
    layout = layout.replace(
        'android:id="@+id/distanceGroup"',
        'android:id="@+id/distanceGroup"\n            android:clipChildren="false"\n            android:clipToPadding="false"',
    )
layout_path.write_text(layout, encoding='utf-8')

# 3) Yalnız reset DÜĞMESİNİN listener bloğunu kaldır.
# Uygulamanın çekim sonrası kendi kullandığı reset() fonksiyonuna dokunma.
main_path = project / 'app/src/main/java/com/stereoguide/app/MainActivity.kt'
main = main_path.read_text(encoding='utf-8')
needle = 'binding.reset.setOnClickListener'
pos = main.find(needle)
if pos != -1:
    line_start = main.rfind('\n', 0, pos) + 1
    brace_start = main.find('{', pos)
    if brace_start == -1:
        raise RuntimeError('Reset listener başlangıç parantezi bulunamadı.')
    depth = 0
    i = brace_start
    in_string = False
    escape = False
    while i < len(main):
        ch = main[i]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    block_end = i + 1
                    if block_end < len(main) and main[block_end] == '\r':
                        block_end += 1
                    if block_end < len(main) and main[block_end] == '\n':
                        block_end += 1
                    main = main[:line_start] + main[block_end:]
                    break
        i += 1
    else:
        raise RuntimeError('Reset listener kapanış parantezi bulunamadı.')

main = re.sub(r'(?m)^.*binding\.reset(?:\.|\b).*$\n?', '', main)
if 'binding.reset' in main:
    raise RuntimeError('MainActivity içinde reset düğmesi referansı kaldı.')
main_path.write_text(main, encoding='utf-8')

# 4) Reset düğmesine özel kaynakları kaldır.
strings_path = res / 'values/strings.xml'
strings = strings_path.read_text(encoding='utf-8')
strings = re.sub(r'\s*<string\s+name="reset">.*?</string>', '', strings, flags=re.S)
strings_path.write_text(strings, encoding='utf-8')
restart_icon = res / 'drawable/ic_restart.xml'
if restart_icon.exists():
    restart_icon.unlink()

# 5) Daha görünür ama abartısız 3D/kabartma.
animator_dir = res / 'animator'
animator_dir.mkdir(parents=True, exist_ok=True)
(animator_dir / 'button_elevation.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true">
        <objectAnimator android:duration="70" android:propertyName="translationZ" android:valueTo="0dp" android:valueType="floatType" />
    </item>
    <item android:state_checked="true">
        <objectAnimator android:duration="130" android:propertyName="translationZ" android:valueTo="10dp" android:valueType="floatType" />
    </item>
    <item>
        <objectAnimator android:duration="130" android:propertyName="translationZ" android:valueTo="2dp" android:valueType="floatType" />
    </item>
</selector>
''', encoding='utf-8')

themes_path = res / 'values/themes.xml'
themes = themes_path.read_text(encoding='utf-8')
# Önce eski eklemeler varsa normalize et.
themes = re.sub(r'\n\s*<item name="android:elevation">\d+dp</item>', '', themes)
themes = re.sub(r'\n\s*<item name="android:stateListAnimator">@animator/button_elevation</item>', '', themes)
themes = themes.replace('<item name="strokeWidth">1dp</item>', '<item name="strokeWidth">2dp</item>')
themes = themes.replace(
    '<item name="cornerRadius">21dp</item>',
    '<item name="cornerRadius">21dp</item>\n        <item name="android:elevation">5dp</item>\n        <item name="android:stateListAnimator">@animator/button_elevation</item>',
)
themes = themes.replace(
    '<item name="cornerRadius">14dp</item>',
    '<item name="cornerRadius">14dp</item>\n        <item name="android:elevation">5dp</item>\n        <item name="android:stateListAnimator">@animator/button_elevation</item>',
)
themes_path.write_text(themes, encoding='utf-8')

# 6) Sürümü artır.
gradle_path = project / 'app/build.gradle.kts'
gradle = gradle_path.read_text(encoding='utf-8')
gradle = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 11', gradle)
gradle = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "0.9.2"', gradle)
gradle_path.write_text(gradle, encoding='utf-8')

# Son kontrol: eski görünen etiketler layout'ta bulunmamalı.
final_layout = layout_path.read_text(encoding='utf-8')
for bad in ('close_4cm', 'portrait_6cm', 'landscape_8cm', 'macro_12cm', '@string/zoom_wide', '@string/zoom_normal', '@+id/reset'):
    if bad in final_layout:
        raise RuntimeError(f'Eski UI referansı kaldı: {bad}')

print('v0.9.2 hazır: etiketler kesin olarak sade, reset yok, 3D düğmeler güçlendirildi.')
