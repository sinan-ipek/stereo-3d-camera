from pathlib import Path

root = Path('StereoGuide/app/src/main/res')
(root / 'color').mkdir(parents=True, exist_ok=True)
(root / 'drawable').mkdir(parents=True, exist_ok=True)

(root / 'layout/activity_main.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/black">

    <androidx.camera.view.PreviewView
        android:id="@+id/preview"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintDimensionRatio="9:16"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toTopOf="@id/controls"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:scaleType="fillCenter" />

    <ImageView
        android:id="@+id/ghost"
        android:layout_width="0dp"
        android:layout_height="0dp"
        android:alpha="0.34"
        android:contentDescription="@string/ghost_description"
        android:scaleType="centerCrop"
        android:visibility="gone"
        app:layout_constraintTop_toTopOf="@id/preview"
        app:layout_constraintBottom_toBottomOf="@id/preview"
        app:layout_constraintStart_toStartOf="@id/preview"
        app:layout_constraintEnd_toEndOf="@id/preview" />

    <com.stereoguide.app.GuideOverlayView
        android:id="@+id/guide"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintTop_toTopOf="@id/preview"
        app:layout_constraintBottom_toBottomOf="@id/preview"
        app:layout_constraintStart_toStartOf="@id/preview"
        app:layout_constraintEnd_toEndOf="@id/preview" />

    <LinearLayout
        android:id="@+id/statusCard"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="16dp"
        android:layout_marginTop="16dp"
        android:layout_marginEnd="16dp"
        android:background="@drawable/status_background"
        android:elevation="6dp"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:padding="12dp"
        app:layout_constraintTop_toTopOf="@id/preview"
        app:layout_constraintStart_toStartOf="@id/preview"
        app:layout_constraintEnd_toEndOf="@id/preview">

        <ImageView
            android:layout_width="24dp"
            android:layout_height="24dp"
            android:src="@drawable/ic_stereo"
            android:contentDescription="@null"
            app:tint="@color/accent_light" />

        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginStart="12dp"
            android:layout_weight="1"
            android:orientation="vertical">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="@string/app_name"
                android:textColor="@color/white"
                android:textSize="15sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/status"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="2dp"
                android:text="@string/first_photo"
                android:textColor="@color/text_secondary"
                android:textSize="13sp" />
        </LinearLayout>
    </LinearLayout>

    <com.google.android.material.button.MaterialButtonToggleGroup
        android:id="@+id/zoomGroup"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="14dp"
        android:elevation="8dp"
        app:checkedButton="@id/zoomNormal"
        app:selectionRequired="true"
        app:singleSelection="true"
        app:layout_constraintBottom_toBottomOf="@id/preview"
        app:layout_constraintStart_toStartOf="@id/preview"
        app:layout_constraintEnd_toEndOf="@id/preview">

        <com.google.android.material.button.MaterialButton
            android:id="@+id/zoomWide"
            style="@style/StereoGuide.ZoomButton"
            android:layout_width="64dp"
            android:layout_height="42dp"
            android:text="@string/zoom_wide" />

        <com.google.android.material.button.MaterialButton
            android:id="@+id/zoomNormal"
            style="@style/StereoGuide.ZoomButton"
            android:layout_width="64dp"
            android:layout_height="42dp"
            android:text="@string/zoom_normal" />
    </com.google.android.material.button.MaterialButtonToggleGroup>

    <LinearLayout
        android:id="@+id/controls"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:background="@drawable/panel_background"
        android:gravity="center_horizontal"
        android:orientation="vertical"
        android:paddingStart="14dp"
        android:paddingTop="14dp"
        android:paddingEnd="14dp"
        android:paddingBottom="24dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/stereo_mode"
            android:textColor="@color/text_muted"
            android:textSize="11sp"
            android:textStyle="bold"
            android:letterSpacing="0.12" />

        <com.google.android.material.button.MaterialButtonToggleGroup
            android:id="@+id/distanceGroup"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            app:checkedButton="@id/portrait"
            app:selectionRequired="true"
            app:singleSelection="true">

            <com.google.android.material.button.MaterialButton
                android:id="@+id/close"
                style="@style/StereoGuide.ModeButton"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="@string/close_4cm" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/portrait"
                style="@style/StereoGuide.ModeButton"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="@string/portrait_6cm" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/landscape"
                style="@style/StereoGuide.ModeButton"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="@string/landscape_8cm" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/macro"
                style="@style/StereoGuide.ModeButton"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="@string/macro_12cm" />
        </com.google.android.material.button.MaterialButtonToggleGroup>

        <androidx.constraintlayout.widget.ConstraintLayout
            android:layout_width="match_parent"
            android:layout_height="92dp"
            android:layout_marginTop="8dp">

            <com.google.android.material.button.MaterialButton
                android:id="@+id/reset"
                style="@style/Widget.MaterialComponents.Button.TextButton"
                android:layout_width="58dp"
                android:layout_height="58dp"
                android:contentDescription="@string/reset"
                android:insetLeft="0dp"
                android:insetTop="0dp"
                android:insetRight="0dp"
                android:insetBottom="0dp"
                android:minWidth="0dp"
                android:padding="15dp"
                app:backgroundTint="@color/control_circle"
                app:cornerRadius="29dp"
                app:icon="@drawable/ic_restart"
                app:iconGravity="textStart"
                app:iconPadding="0dp"
                app:iconSize="25dp"
                app:iconTint="@color/white"
                app:layout_constraintTop_toTopOf="parent"
                app:layout_constraintBottom_toBottomOf="parent"
                app:layout_constraintStart_toStartOf="parent" />

            <FrameLayout
                android:id="@+id/shutterContainer"
                android:layout_width="82dp"
                android:layout_height="82dp"
                app:layout_constraintTop_toTopOf="parent"
                app:layout_constraintBottom_toBottomOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintEnd_toEndOf="parent">

                <View
                    android:layout_width="82dp"
                    android:layout_height="82dp"
                    android:background="@drawable/shutter_outer" />

                <com.google.android.material.button.MaterialButton
                    android:id="@+id/shutter"
                    android:layout_width="66dp"
                    android:layout_height="66dp"
                    android:layout_gravity="center"
                    android:contentDescription="@string/shoot"
                    android:insetLeft="0dp"
                    android:insetTop="0dp"
                    android:insetRight="0dp"
                    android:insetBottom="0dp"
                    android:minWidth="0dp"
                    android:minHeight="0dp"
                    android:padding="0dp"
                    android:text=""
                    app:backgroundTint="@color/shutter_inner"
                    app:cornerRadius="33dp"
                    app:rippleColor="@color/shutter_ripple" />
            </FrameLayout>
        </androidx.constraintlayout.widget.ConstraintLayout>
    </LinearLayout>
</androidx.constraintlayout.widget.ConstraintLayout>
''')

(root / 'values/colors.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#05070A</color>
    <color name="white">#FFFFFFFF</color>
    <color name="panel">#F20B0F14</color>
    <color name="panel_border">#263544</color>
    <color name="status_card">#B20A0E14</color>
    <color name="status_border">#34485E</color>
    <color name="text_secondary">#D5DEE8</color>
    <color name="text_muted">#8291A3</color>
    <color name="accent">#2D83FF</color>
    <color name="accent_dark">#1666D8</color>
    <color name="accent_light">#74B4FF</color>
    <color name="outline">#465565</color>
    <color name="control_circle">#26303B</color>
    <color name="shutter_outer">#F4F7FA</color>
    <color name="shutter_inner">#FFFFFF</color>
    <color name="shutter_ripple">#90B8DCFF</color>
</resources>
''')

(root / 'values/themes.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.StereoGuide" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/accent</item>
        <item name="colorPrimaryVariant">@color/accent_dark</item>
        <item name="colorSecondary">@color/accent_light</item>
        <item name="colorSurface">@color/panel</item>
        <item name="colorOnPrimary">@color/white</item>
        <item name="colorOnSurface">@color/white</item>
        <item name="android:statusBarColor">@android:color/transparent</item>
        <item name="android:navigationBarColor">@color/black</item>
        <item name="android:windowLightStatusBar" tools:targetApi="23">false</item>
        <item name="android:windowLightNavigationBar" tools:targetApi="27">false</item>
    </style>

    <style name="StereoGuide.ZoomButton" parent="Widget.MaterialComponents.Button.OutlinedButton">
        <item name="android:minWidth">0dp</item>
        <item name="android:textAllCaps">false</item>
        <item name="android:textStyle">bold</item>
        <item name="android:textSize">14sp</item>
        <item name="android:textColor">@color/selector_button_text</item>
        <item name="backgroundTint">@color/selector_button_background</item>
        <item name="strokeColor">@color/selector_button_stroke</item>
        <item name="strokeWidth">1dp</item>
        <item name="cornerRadius">21dp</item>
        <item name="android:insetLeft">0dp</item>
        <item name="android:insetRight">0dp</item>
        <item name="android:insetTop">0dp</item>
        <item name="android:insetBottom">0dp</item>
    </style>

    <style name="StereoGuide.ModeButton" parent="Widget.MaterialComponents.Button.OutlinedButton">
        <item name="android:minWidth">0dp</item>
        <item name="android:textAllCaps">false</item>
        <item name="android:textStyle">bold</item>
        <item name="android:textSize">12sp</item>
        <item name="android:textColor">@color/selector_button_text</item>
        <item name="backgroundTint">@color/selector_button_background</item>
        <item name="strokeColor">@color/selector_button_stroke</item>
        <item name="strokeWidth">1dp</item>
        <item name="cornerRadius">14dp</item>
        <item name="android:insetLeft">0dp</item>
        <item name="android:insetRight">0dp</item>
        <item name="android:insetTop">0dp</item>
        <item name="android:insetBottom">0dp</item>
    </style>
</resources>
''')

(root / 'color/selector_button_background.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_enabled="false" android:color="#18202A" />
    <item android:state_checked="true" android:color="@color/accent" />
    <item android:color="#99161D26" />
</selector>
''')
(root / 'color/selector_button_text.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_enabled="false" android:color="#53606F" />
    <item android:state_checked="true" android:color="@color/white" />
    <item android:color="@color/text_secondary" />
</selector>
''')
(root / 'color/selector_button_stroke.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_enabled="false" android:color="#26303A" />
    <item android:state_checked="true" android:color="@color/accent_light" />
    <item android:color="@color/outline" />
</selector>
''')

(root / 'drawable/status_background.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="@color/status_card" />
    <stroke android:width="1dp" android:color="@color/status_border" />
    <corners android:radius="18dp" />
</shape>
''')
(root / 'drawable/panel_background.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="@color/panel" />
    <stroke android:width="1dp" android:color="@color/panel_border" />
    <corners android:topLeftRadius="26dp" android:topRightRadius="26dp" />
</shape>
''')
(root / 'drawable/shutter_outer.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <solid android:color="@android:color/transparent" />
    <stroke android:width="4dp" android:color="@color/shutter_outer" />
</shape>
''')
(root / 'drawable/ic_restart.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="@android:color/white" android:pathData="M12,5C8.69,5 6,7.69 6,11C6,14.31 8.69,17 12,17C14.61,17 16.83,15.33 17.65,13L19.74,13C18.83,16.45 15.69,19 12,19C7.58,19 4,15.42 4,11C4,6.58 7.58,3 12,3C14.21,3 16.21,3.9 17.66,5.34L20,3L20,9L14,9L16.24,6.76C15.15,5.67 13.65,5 12,5Z" />
</vector>
''')
(root / 'drawable/ic_stereo.xml').write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="@android:color/white" android:pathData="M7.5,5C3.91,5 1,7.91 1,11.5C1,15.09 3.91,18 7.5,18C9.25,18 10.83,17.31 12,16.19C13.17,17.31 14.75,18 16.5,18C20.09,18 23,15.09 23,11.5C23,7.91 20.09,5 16.5,5C14.75,5 13.17,5.69 12,6.81C10.83,5.69 9.25,5 7.5,5ZM7.5,7C9.99,7 12,9.01 12,11.5C12,13.99 9.99,16 7.5,16C5.01,16 3,13.99 3,11.5C3,9.01 5.01,7 7.5,7ZM16.5,7C18.99,7 21,9.01 21,11.5C21,13.99 18.99,16 16.5,16C14.01,16 12,13.99 12,11.5C12,9.01 14.01,7 16.5,7Z" />
</vector>
''')

strings = root / 'values/strings.xml'
s = strings.read_text()
if '<string name="stereo_mode">' not in s:
    s = s.replace('</resources>', '    <string name="stereo_mode">STEREO MODU</string>\n</resources>')
s = s.replace('Makro 12 cm', 'Hiper')
strings.write_text(s)

gradle = Path('StereoGuide/app/build.gradle.kts')
g = gradle.read_text().replace('versionCode = 8', 'versionCode = 10').replace('versionCode = 9', 'versionCode = 10').replace('versionName = "0.8.0"', 'versionName = "0.9.0"').replace('versionName = "0.8.1"', 'versionName = "0.9.0"')
gradle.write_text(g)
