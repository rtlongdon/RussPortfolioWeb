# Manual Screenshots

Drop screenshots here for `../USER_MANUAL_DRAFT.md`. The manual already
references the filenames below by name — just save a capture with the
matching filename and it'll pick up automatically, no markdown edits needed.

## Capturing

- **Physical device:** Power + Volume-down (or your device's usual
  screenshot gesture), then transfer the PNG here.
- **Emulator (Android Studio):** camera icon in the emulator toolbar.
- **adb:** `adb shell screencap -p /sdcard/screen.png` then
  `adb pull /sdcard/screen.png`.

## Expected filenames

Full-screen device captures are cropped down to the relevant region(s) and
resized to 720px wide before going in the manual (see "Cropping/resizing"
below) — several filenames below are crops derived from a single raw
capture, not independent screenshots.

| Filename | Screen / region | Manual section | Status |
|---|---|---|---|
| `profile_selection.png` | Profile Selection ("Select Approach Profile") | Section 4 | ✅ captured |
| `adhoc_setup.png` | AD HOC APPROACH SETUP | Section 4 | ✅ captured |
| `detailed_editor.png` | Create/Edit Approach Profile, top of form | Section 4 | ✅ captured |
| `detailed_editor_dh_field.png` | Create/Edit Approach Profile, scrolled to DH field | Section 5 | ✅ captured |
| `hsi_gauge.png` | Main flying screen, HSI gauge mode — gauge only, cropped | Section 3 | ✅ captured + cropped |
| `vor_gauge.png` | Main flying screen, VOR/CDI gauge mode — gauge only, cropped | Section 3 | ✅ captured + cropped |
| `plan_view.png` | Bottom half, plan view only — cropped from the `hsi_gauge.png` raw capture | Section 3 | ✅ captured + cropped |
| `profile_strip.png` | Bottom half, profile strip + MAP card — cropped from the `hsi_gauge.png` raw capture | Section 3 | ✅ captured + cropped |
| `corridor_view.png` | Bottom half, corridor view only — cropped | Section 3 | ✅ captured + cropped |
| `vor_approach.png` | Flying a real VOR approach — gauge only (bearing needle, TO/FROM), cropped | Section 5 | ✅ captured + cropped |
| `vor_approach_plan.png` | Same VOR approach — plan view only (cone of confusion), cropped | Section 5 | ✅ captured + cropped |
| `ndb_approach.png` | Flying a real NDB approach — gauge only, cropped | Section 5 | ✅ captured + cropped (recaptured 2026-07-19 after fixing a TO/FROM-on-NDB bug in `VorGauge.kt`) |
| `ils_practice.png` | ILS Practice Mode, mode-selection screen (pre-START) | Section 6 | ✅ captured |
| `ils_practice_flying.png` | ILS Practice Mode, in flight (sensitivity, CRS/offset readouts) | Section 6 | ✅ captured |
| `datastream_debug.png` | Settings → Debug → Datastream Debug | Section 9 | ✅ captured |

Add more rows here (and a matching `![...]()` line in the manual) if we
decide to cover additional screens later — e.g. individual ILS Practice
sensitivity presets, the missed-approach MAP card close-up, etc.

## Cropping/resizing

Full-device captures are 1200x1920. The gauge/plan-view/profile-strip
boundaries are consistent across captures (same device, same layout), so
new full-screen shots can be re-cropped with the same boxes:

| Region | Crop box (x0, y0, x1, y1) |
|---|---|
| Gauge | `(0, 0, 1200, 960)` |
| Plan view (circular) | `(0, 960, 1200, 1400)` |
| Corridor view | `(0, 960, 1200, 1205)` |
| Profile strip (incl. MAP card) | `(0, 1400, 1200, 1900)` |

Done with Python/Pillow: crop, then resize to 720px wide (preserving aspect
ratio) if wider than that. No fixed script lives in the repo for this yet —
it was run ad hoc; worth turning into a small script here if we do this
often enough to justify it.
