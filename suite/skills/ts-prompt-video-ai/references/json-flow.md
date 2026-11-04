# Schema JSON cho từng cảnh (Flow / Veo và công cụ video AI tương tự)

Quy tắc ngôn ngữ:
- **Toàn bộ mô tả viết bằng tiếng Anh** (công cụ video AI hiểu tiếng Anh tốt nhất).
- **Chỉ `dialogue.text` giữ nguyên tiếng Việt có dấu** — đúng lời thoại trong kịch bản.
- Chữ hiện trên màn hình (nếu người dùng yêu cầu) ghi đúng tiếng Việt có dấu trong `on_screen_text`.

Mỗi cảnh là một object độc lập, xuất trong **một khối mã `json` riêng**:

```json
{
  "scene_id": "S01",
  "duration_seconds": 8,
  "aspect_ratio": "9:16",
  "reference_images": {
    "character": "Match the uploaded character reference photo exactly",
    "product": "Match the uploaded product reference photo exactly"
  },
  "continuity": "Keep the same face, hair, age, outfit, body proportions, product, logo, colors and lighting as the previous scene",
  "setting": "Bright modern bakery counter in the morning, pastel walls, glass display of cakes in the background",
  "subject": "Vietnamese woman in her early 30s, shoulder-length black hair, white blouse, beige trousers, nude flats, warm friendly smile; holding the strawberry birthday cake from the product reference",
  "action": "She lifts the cake box lid toward the camera and smiles; one main natural action only",
  "camera": {
    "shot": "medium close-up",
    "movement": "slow push-in",
    "lens_feel": "natural commercial look, shallow depth of field"
  },
  "lighting": "Soft natural window light from the left, warm tone, consistent across scenes",
  "dialogue": {
    "language": "vi-VN",
    "text": "Bánh sinh nhật giao đúng giờ, đúng mẫu, bé nhà mình chắc chắn sẽ thích.",
    "speaker": "the woman in the scene",
    "voice": "Southern Vietnamese female voice, warm, energetic, medium pace",
    "voice_consistency": "Same voice, pace and emotion across all scenes",
    "lip_sync": true
  },
  "audio": {
    "dialogue_priority": true,
    "ambient_sound": "Quiet bakery ambience, soft chatter far away, lower than the voice",
    "sound_effects": ["soft paper rustle when the box opens"],
    "background_music": false,
    "music": "none"
  },
  "on_screen_text": "",
  "negative_constraints": [
    "no music",
    "no background score",
    "do not generate music",
    "do not alter the reference character",
    "do not alter product shape, color, logo, label or text",
    "no face distortion",
    "no extra fingers",
    "no unreadable text",
    "no subtitles unless explicitly requested"
  ],
  "transition": "Cut on action to S02 as she places the cake on the counter"
}
```

## Quy tắc từng trường

| Trường | Bắt buộc | Ghi chú |
|---|---|---|
| `scene_id` | ✔ | S01, S02… theo thứ tự |
| `duration_seconds` | ✔ | Mặc định 8 (theo độ dài clip của công cụ; người dùng chọn khác thì sửa) |
| `aspect_ratio` | ✔ | `9:16` (dọc) hoặc `16:9` (ngang), giống nhau mọi cảnh |
| `reference_images` | ✔ khi có ảnh | Không có ảnh sản phẩm → bỏ khóa `product`, mô tả sản phẩm kỹ trong `subject` |
| `continuity` | ✔ | Luôn nhắc giữ nguyên nhân vật/sản phẩm/ánh sáng |
| `subject` | ✔ | Lấy mô tả nhân vật + trang phục từ `04-thuong-hieu-noi-dung.md` (dòng "Mô tả tiếng Anh cho AI") nếu có |
| `action` | ✔ | **Một** hành động chính, làm được trong 8 giây |
| `dialogue.text` | ✔ | Tiếng Việt; khoảng 18–22 từ/8 giây; cảnh không thoại → chuỗi rỗng `""` |
| `dialogue.voice` | ✔ | Giọng lấy từ tệp 04 (vùng miền, tốc độ, cảm xúc) |
| `audio.background_music` | ✔ | **Luôn `false`** |
| `audio.music` | ✔ | **Luôn `"none"`** |
| `audio.ambient_sound`, `sound_effects` | ✔ | Mô tả cụ thể, nhỏ hơn giọng nói; không ghi chung chung "cinematic audio" |
| `on_screen_text` | tùy | Chỉ khi người dùng yêu cầu chữ trên hình; tiếng Việt đúng dấu, ngắn |
| `negative_constraints` | ✔ | Luôn có đủ 3 lệnh cấm nhạc: `no music`, `no background score`, `do not generate music` |

Nếu cảnh không có thoại: giữ `dialogue.text` là `""`, vẫn để `background_music: false`, `music: "none"`.

## Bản rút gọn (cho công cụ giới hạn độ dài lệnh)

Một số công cụ video AI từ chối lệnh dài. Khi người dùng chọn "bản rút gọn", giữ đủ ý chính trong một đoạn
tiếng Anh ngắn (khoảng một nửa độ dài), lời thoại vẫn tiếng Việt:

```text
9:16, 8s. Same woman as reference photo (early 30s, black shoulder-length hair, white blouse, beige trousers).
Bakery counter, soft window light. She opens the cake box toward camera, smiles. Slow push-in, medium close-up.
She says in Vietnamese (Southern accent, warm): "Bánh sinh nhật giao đúng giờ, đúng mẫu, bé nhà mình chắc chắn sẽ thích."
Quiet bakery ambience. No music, no background score, do not generate music. Keep face and product unchanged.
```

## Từ ngữ dễ bị công cụ chặn

Nếu công cụ báo vi phạm chính sách, giữ nguyên ý nhưng đổi cách diễn đạt trong phần mô tả tiếng Anh
(không đổi lời thoại khi không cần):
- Cảnh có trẻ em → mô tả trung tính, trang phục kín đáo, bối cảnh gia đình.
- Từ chỉ bạo lực/cơ thể nhạy cảm → dùng từ trung tính ("tired", "concerned" thay cho mô tả cực đoan).
- Tên người nổi tiếng/thương hiệu khác → bỏ, mô tả chung.
