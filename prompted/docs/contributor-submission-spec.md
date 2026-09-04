# Prompted Contributor Submission Spec

Technical requirements for photographers submitting frames to the Prompted pose reference library. Read the [contributor license](contributor-license.md) and the [model release](model-release.md) first; both need to be in place before anything is published.

## What to send

- **Set size:** 10 to 15 frames per submission. Fewer is fine for a first look; the lifetime Pro grant applies to an accepted set of 10 to 15.
- **Where:** email support@cooperindustries.cc with the subject **"Prompted contributor"** and a link to the frames (Dropbox, Google Drive, iCloud, WeTransfer, or similar). Do not attach the images to the email.
- **With the frames:** the metadata sheet described below (CSV or a spreadsheet link), and your credit name.

## Image requirements

| Requirement | Detail |
|---|---|
| Format | JPEG or HEIC |
| Size | 1200 x 1500 px minimum. Larger is welcome; we downsample. |
| Orientation | Portrait 4:5 preferred. Landscape accepted for a small number of poses; we crop to 4:5 for the app where possible. |
| Colour | sRGB or Display P3. No CMYK. |
| EXIF | **Strip all EXIF metadata before sending** (location, camera serial, timestamps). On a Mac: Preview > Tools > Show Inspector, or `exiftool -all= file.jpg`. On iPhone: Photos > share > Options > turn off Location and All Photos Data. |
| One pose per frame | Each frame shows a single, clearly readable pose. No diptychs, collages, or contact sheets. |
| Watermarks | None. No logos, borders, or text overlays. |
| Processing | Normal edit only. No heavy filters, film presets that crush shadows, heavy grain, split toning, or AI enhancement. Skin should look like skin. |
| Sharpness | Subjects sharp, especially faces and hands. Motion blur only if it is the point of the pose. |
| Subjects | Everyone identifiable in frame has a signed model release. Frames with unreleased bystanders will be declined. |
| Filenames | `lastname-category-NN.jpg`, for example `cooper-couples-03.jpg`. |

## Per-image metadata

Supply one row per frame with these fields. Values must match the vocabularies below exactly (lower case, underscores).

| Column | Values |
|---|---|
| `filename` | The filename as sent |
| `category` | `couples`, `engagement`, `family`, `maternity`, `senior` |
| `subject_count` | Integer, number of people in frame |
| `light` | `golden`, `blue`, `soft_low`, `mid`, `harsh_overhead`, `overcast`, `open_shade`, `backlit`, `indoor_window`, `night_flash` |
| `location` | `beach`, `forest`, `urban`, `field`, `studio`, `home`, `mountain` |
| `release_on_file` | `yes` or `no`. Must be `yes` for every identifiable person, including a guardian signature for minors. |
| `notes` | Optional. Anything we should know: the prompt you used, accessibility notes (seated, plus-size, wheelchair, late-term), what makes the pose work. |

### Light vocabulary

| Value | Meaning |
|---|---|
| `golden` | Sun low, within about an hour of sunrise or sunset, warm directional light |
| `blue` | After sunset or before sunrise, soft cool ambient |
| `soft_low` | Sun low but diffused, mild direction, no hard shadows |
| `mid` | Mid-morning or mid-afternoon sun, moderate elevation |
| `harsh_overhead` | Midday sun, hard shadows under eyes and nose |
| `overcast` | Cloud cover, flat and even |
| `open_shade` | Subject in shade, lit by open sky |
| `backlit` | Sun behind the subject, rim light or flare |
| `indoor_window` | Indoors, natural window light |
| `night_flash` | Night or dark interior, on- or off-camera flash |

### CSV template

Copy this header row and one line per frame. A Google Sheet or Numbers document with the same columns is fine.

```csv
filename,category,subject_count,light,location,release_on_file,notes
cooper-couples-01.jpg,couples,2,golden,field,yes,"Foreheads together, eyes closed"
cooper-couples-02.jpg,couples,2,backlit,beach,yes,
cooper-family-01.jpg,family,4,open_shade,forest,yes,"Grandparent seated"
cooper-senior-01.jpg,senior,1,indoor_window,home,yes,"Minor; guardian release on file"
```

## Review

1. **Curation.** We look at the set as a whole and pick frames that show a pose the app does not already cover, read clearly at phone size, and match the light and location you tagged. Expect some declines; a strong set of 15 might yield 10.
2. **Prompts are ours.** We write the setup steps and the three verbal prompts (playful, romantic, nervous client) for every pose in the library, in the app's voice. Your notes help; you do not need to write prompts.
3. **Credit preview.** Before anything goes live you receive a preview of each accepted pose with your credit line as it will appear ("Photo: <name>"). Correct it then if needed.
4. **Publish.** Accepted frames ship in the next catalog update. Your Prompted Pro lifetime grant is applied to the Apple Account you gave us on the license, usually within a week of acceptance.
5. **Declined frames** are deleted from our systems and are not covered by the license.

Questions: support@cooperindustries.cc
