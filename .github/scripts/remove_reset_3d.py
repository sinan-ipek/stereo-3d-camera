from pathlib import Path
import re

project = Path('StereoGuide')
res = project / 'app/src/main/res'

# 1) Mod adlarını sadeleştir: ekranda cm gösterme.
strings_path = res / 'values/strings.xml'
strings = strings_path.read_text(encoding='utf-8')
replacements = {
    'close_4cm': 'Yakın',
    'portrait_6cm': 'Portre',
    'landscape_8cm': 'Uzak',
    'macro_12cm': 'Hiper',
}
for key, value in replacements.items():
    strings = re.sub(
        rf'<string\s+name="{re.escape(key)}">.*?</string>',
        f'<string name="{key}">{value}</string>',
        strings,
        flags=re.S,
    )

# 2) Sıfırla / yeniden dene düğmesini arayüzden tamamen kaldır.
layout_path = res / 'layout/activity_main.xml'
layout = layout_path.read_text(encoding='utf-8')
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

# Toggle gruplarında yükseltilmiş düğme gölgelerinin kesilmesini önle.
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

# 3) Reset düğmesinin click-handler / doğrudan view kodunu kaldır.
main_path = project / 'app/src/main/java/com/stereoguide/app/MainActivity.kt'
main = main_path.read_text(encoding='utf-8')
main = re.sub(
    r'(?ms)^\s*binding\.reset\.setOnClickListener\s*\{.*?^\s*\}\s*\n',
    '',
    main,
)
main = re.sub(r'(?m)^.*binding\.reset.*\n?', '', main)
if 'binding.reset' in main:
    raise RuntimeError('MainActivity içinde reset düğmesi referansı kaldı.')
main_path.write_text(main, encoding='utf-8')

# 4) Reset kaynaklarını ancak UI ve kod referansları kaldırıldıktan sonra sil.
strings = strings_path.read_text(encoding='utf-8')
strings = re.sub(r'\s*<string\s+name="reset">.*?</string>', '', strings, flags=re.S)
strings_path.write_text(strings, encoding='utf-8')
restart_icon = res / 'drawable/ic_restart.xml'
if restart_icon.exists():
    restart_icon.unlink()

# 5) Hafif 3D/kabartma: taban elevation + seçilince yükselme.
animator_dir = res / 'animator'
animator_dir.mkdir(parents=True, exist_ok=True)
(animator_dir / 'button_elevation.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true">
        <objectAnimator
            android:duration="90"
            android:propertyName="translationZ"
            android:valueTo="1dp"
            android:valueType="floatType" />
    </item>
    <item android:state_checked="true">
        <objectAnimator
            android:duration="140"
            android:propertyName="translationZ"
            android:valueTo="6dp"
            android:valueType="floatType" />
    </item>
    <item>
        <objectAnimator
            android:duration="140"
            android:propertyName="translationZ"
            android:valueTo="0dp"
            android:valueType="floatType" />
    </item>
</selector>
''', encoding='utf-8')

themes_path = res / 'values/themes.xml'
themes = themes_path.read_text(encoding='utf-8')
if '@animator/button_elevation' not in themes:
    themes = themes.replace(
        '<item name="cornerRadius">21dp</item>',
        '<item name="cornerRadius">21dp</item>\n        <item name="android:elevation">3dp</item>\n        <item name="android:stateListAnimator">@animator/button_elevation</item>',
    )
    themes = themes.replace(
        '<item name="cornerRadius">14dp</item>',
        '<item name="cornerRadius">14dp</item>\n        <item name="android:elevation">3dp</item>\n        <item name="android:stateListAnimator">@animator/button_elevation</item>',
    )
themes_path.write_text(themes, encoding='utf-8')

# Sürümü artır.
gradle_path = project / 'app/build.gradle.kts'
gradle = gradle_path.read_text(encoding='utf-8')
gradle = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 10', gradle)
gradle = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "0.9.1"', gradle)
gradle_path.write_text(gradle, encoding='utf-8')

print('v0.9.1 hazır: Yakın/Portre/Uzak/Hiper, reset tamamen silindi, hafif 3D düğmeler eklendi.')
