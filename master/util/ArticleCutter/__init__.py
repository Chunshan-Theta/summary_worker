import os
import math
import pathlib


def load_model():
  base_path = pathlib.Path(__file__).parent.resolve()
  models = [f"{base_path}/{i}" for i in os.listdir(base_path) if i.endswith(".cw")]
  load_model = {}

  for name in models:
      with open(name,"r") as f:
        for line in f.readlines():
          label, score = line.replace("\n","").split(":")
          score = float(score)
          load_model[label]=score
  return load_model

def interface_convolution(sent: str, threshold=0.3, min_windows_size=3, max_windows_size=9, return_score=False):
  def window_score(text, center_idx, width):
    half_width = int(width / 2 - 0.5)

    # left_label
    left_score = 0
    if center_idx - half_width + 1 > 0:
      left_label = text[center_idx - half_width + 1:center_idx + 1] + "^"
      if left_label in model:
        left_score = model[left_label]
    else:
      left_score = -1

    # right_label
    right_score = 0
    if center_idx + half_width + 1 <= len(text):
      right_label = "^" + text[center_idx + 1:center_idx + half_width + 1]

      if right_label in model:
        right_score = model[right_label]
    else:
      right_score = -1

    # center_label
    center_label = text[center_idx - half_width + 1:center_idx + 1] + "^" + text[
                                                                            center_idx + 1:center_idx + half_width + 1]
    center_score = 0
    if center_label in model:
      center_score = model[center_label]

    # print(left_score,right_score,center_score)
    return (left_score + right_score) * 0.2 + center_score * 0.6
  # print(sent)
  #
  if len(sent) < max_windows_size:
    if return_score:
      return [0] * len(sent)
    return sent

  #
  sub_sents_array = []
  sub_sent_temp = ""
  for idx in range(0, len(sent)):
    sub_sent_temp += sent[idx]

    #
    score = 0
    for width in range(min_windows_size, max_windows_size + 2, 2):
      score += (window_score(sent, idx, width)) * (width / max_windows_size)
    score /= len(range(min_windows_size, max_windows_size + 2, 2))

    #
    if score > threshold:
      if return_score:
        sub_sents_array.append((sub_sent_temp, score))
      else:
        sub_sents_array.append(sub_sent_temp)
      sub_sent_temp = ""
  sub_sents_array.append(sub_sent_temp)
  return sub_sents_array

model = load_model()
text = "其實你很棒知道自己因為害怕別人的眼光而造就自己體貼的個性或許這樣的性格也是讓你更懂得應對進退至於緊張的狀況下次感受到大家的注目試著先閉上眼睛深呼吸告訴自己沒問題然後再張開眼睛開始動作也許就能緩解那種緊張心情喔"
print(interface_convolution(text))