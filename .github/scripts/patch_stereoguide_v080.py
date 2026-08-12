from pathlib import Path

ROOT = Path("StereoGuide")
MAIN = ROOT / "app/src/main/java/com/stereoguide/app/MainActivity.kt"
LAYOUT = ROOT / "app/src/main/res/layout/activity_main.xml"
STRINGS = ROOT / "app/src/main/res/values/strings.xml"
GRADLE = ROOT / "app/build.gradle.kts"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Beklenen bölüm bulunamadı: {label}")
    return text.replace(old, new, 1)


def patch_strings() -> None:
    text = STRINGS.read_text(encoding="utf-8")
    old = '    <string name="landscape_8cm">Uzak 8 cm</string>\n'
    new = (
        old
        + '    <string name="macro_12cm">Makro 12 cm</string>\n'
        + '    <string name="zoom_wide">0.6×</string>\n'
        + '    <string name="zoom_normal">1×</string>\n'
    )
    STRINGS.write_text(replace_once(text, old, new, "strings"), encoding="utf-8")


def patch_layout() -> None:
    text = LAYOUT.read_text(encoding="utf-8")

    distance_group_start = '''        <com.google.android.material.button.MaterialButtonToggleGroup
            android:id="@+id/distanceGroup"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            app:singleSelection="true"
            app:selectionRequired="true"
            app:checkedButton="@id/portrait">
'''

    zoom_and_distance = '''        <com.google.android.material.button.MaterialButtonToggleGroup
            android:id="@+id/zoomGroup"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginBottom="8dp"
            app:singleSelection="true"
            app:selectionRequired="true"
            app:checkedButton="@id/zoomNormal">

            <com.google.android.material.button.MaterialButton
                android:id="@+id/zoomWide"
                style="@style/Widget.MaterialComponents.Button.OutlinedButton"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="@string/zoom_wide" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/zoomNormal"
                style="@style/Widget.MaterialComponents.Button.OutlinedButton"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="@string/zoom_normal" />
        </com.google.android.material.button.MaterialButtonToggleGroup>

        <com.google.android.material.button.MaterialButtonToggleGroup
            android:id="@+id/distanceGroup"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            app:singleSelection="true"
            app:selectionRequired="true"
            app:checkedButton="@id/portrait">
'''
    text = replace_once(text, distance_group_start, zoom_and_distance, "zoom group")

    replacements = {
        "close": "@string/close_4cm",
        "portrait": "@string/portrait_6cm",
        "landscape": "@string/landscape_8cm",
    }
    for button_id, string_ref in replacements.items():
        old = f'''            <com.google.android.material.button.MaterialButton
                android:id="@+id/{button_id}"
                style="@style/Widget.MaterialComponents.Button.OutlinedButton"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="{string_ref}" />'''
        new = f'''            <com.google.android.material.button.MaterialButton
                android:id="@+id/{button_id}"
                style="@style/Widget.MaterialComponents.Button.OutlinedButton"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:minWidth="0dp"
                android:textSize="12sp"
                android:text="{string_ref}" />'''
        text = replace_once(text, old, new, f"{button_id} button")

    landscape_button = '''            <com.google.android.material.button.MaterialButton
                android:id="@+id/landscape"
                style="@style/Widget.MaterialComponents.Button.OutlinedButton"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:minWidth="0dp"
                android:textSize="12sp"
                android:text="@string/landscape_8cm" />'''
    macro_button = landscape_button + '''
            <com.google.android.material.button.MaterialButton
                android:id="@+id/macro"
                style="@style/Widget.MaterialComponents.Button.OutlinedButton"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:minWidth="0dp"
                android:textSize="12sp"
                android:text="@string/macro_12cm" />'''
    text = replace_once(text, landscape_button, macro_button, "macro button")

    LAYOUT.write_text(text, encoding="utf-8")


def patch_main() -> None:
    text = MAIN.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "import androidx.camera.core.CameraSelector\n",
        "import androidx.camera.core.Camera\nimport androidx.camera.core.CameraSelector\n",
        "Camera import",
    )

    text = replace_once(
        text,
        "    private var imageCapture: ImageCapture? = null\n",
        "    private var imageCapture: ImageCapture? = null\n"
        "    private var camera: Camera? = null\n"
        "    private var selectedZoomRatio = 1f\n",
        "camera fields",
    )

    old_distance = '''        binding.distanceGroup.addOnButtonCheckedListener { _, checkedId, isChecked ->
            if (!isChecked || firstBurst.isNotEmpty()) return@addOnButtonCheckedListener
            targetCm = when (checkedId) {
                R.id.close -> 4
                R.id.landscape -> 8
                else -> 6
            }
            targetShiftPixels = when (checkedId) {
                R.id.close -> 10
                R.id.landscape -> 5
                else -> 7
            }
        }
'''
    new_distance = '''        binding.distanceGroup.addOnButtonCheckedListener { _, checkedId, isChecked ->
            if (!isChecked || firstBurst.isNotEmpty()) return@addOnButtonCheckedListener
            targetCm = when (checkedId) {
                R.id.close -> 4
                R.id.landscape -> 8
                R.id.macro -> 12
                else -> 6
            }
            targetShiftPixels = when (checkedId) {
                R.id.close -> 10
                R.id.landscape -> 5
                R.id.macro -> 14
                else -> 7
            }
        }

        binding.zoomGroup.addOnButtonCheckedListener { _, checkedId, isChecked ->
            if (!isChecked || firstBurst.isNotEmpty()) return@addOnButtonCheckedListener
            selectedZoomRatio = if (checkedId == R.id.zoomWide) 0.6f else 1f
            applySelectedZoom()
        }
'''
    text = replace_once(text, old_distance, new_distance, "distance listener")

    old_bind = '''            provider.bindToLifecycle(
                this,
                CameraSelector.DEFAULT_BACK_CAMERA,
                preview,
                imageCapture,
                analysis
            )
'''
    new_bind = '''            camera = provider.bindToLifecycle(
                this,
                CameraSelector.DEFAULT_BACK_CAMERA,
                preview,
                imageCapture,
                analysis
            )
            applySelectedZoom()
'''
    text = replace_once(text, old_bind, new_bind, "camera bind")

    capture_marker = "    private fun capture() {\n"
    zoom_method = '''    private fun applySelectedZoom() {
        val activeCamera = camera ?: return
        val zoomState = activeCamera.cameraInfo.zoomState.value ?: return
        val requested = selectedZoomRatio
        if (requested < zoomState.minZoomRatio) {
            selectedZoomRatio = 1f
            binding.zoomWide.isEnabled = false
            if (binding.zoomGroup.checkedButtonId != R.id.zoomNormal) {
                binding.zoomGroup.check(R.id.zoomNormal)
            }
            activeCamera.cameraControl.setZoomRatio(1f.coerceIn(zoomState.minZoomRatio, zoomState.maxZoomRatio))
            return
        }
        binding.zoomWide.isEnabled = true
        activeCamera.cameraControl.setZoomRatio(
            requested.coerceIn(zoomState.minZoomRatio, zoomState.maxZoomRatio)
        )
    }

'''
    text = replace_once(text, capture_marker, zoom_method + capture_marker, "zoom method")

    text = replace_once(
        text,
        "        binding.distanceGroup.isEnabled = false\n",
        "        binding.distanceGroup.isEnabled = false\n        binding.zoomGroup.isEnabled = false\n",
        "disable controls",
    )
    text = replace_once(
        text,
        "        binding.distanceGroup.isEnabled = true\n",
        "        binding.distanceGroup.isEnabled = true\n        binding.zoomGroup.isEnabled = true\n",
        "enable controls",
    )

    MAIN.write_text(text, encoding="utf-8")


def patch_gradle() -> None:
    text = GRADLE.read_text(encoding="utf-8")
    text = replace_once(text, "versionCode = 7", "versionCode = 8", "versionCode")
    text = replace_once(text, 'versionName = "0.7.0"', 'versionName = "0.8.0"', "versionName")
    GRADLE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    patch_strings()
    patch_layout()
    patch_main()
    patch_gradle()
    print("StereoGuide v0.8.0: Makro + 0.6x/1x yaması uygulandı.")
