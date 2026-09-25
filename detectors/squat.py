from core.base_exercise import BaseExercise


class SquatDetector(BaseExercise):
   DOWN_THRESHOLD = 100
   UP_THRESHOLD = 160
   MIN_VISIBILITY = 0.75

   LEFT_HIP = 23
   LEFT_KNEE = 25
   LEFT_ANKLE = 27
   RIGHT_HIP = 24
   RIGHT_KNEE = 26
   RIGHT_ANKLE = 28
   LEFT_SHOULDER = 11
   RIGHT_SHOULDER = 12

   def __init__(self):
      super().__init__()

   def reset(self):
      self.reps = 0
      self.stage = None

   def process(self, landmarks):
      # return super().process(landmarks)
      left_knee_angle = self.calculate_angle(
         self.get_point(landmarks, self.LEFT_HIP),
         self.get_point(landmarks, self.LEFT_KNEE),
         self.get_point(landmarks, self.LEFT_ANKLE)
      )

      right_knee_angle = self.calculate_angle(
         self.get_point(landmarks, self.RIGHT_HIP),
         self.get_point(landmarks, self.RIGHT_KNEE),
         self.get_point(landmarks, self.RIGHT_ANKLE),
      )

      left_visibility = landmarks[self.LEFT_KNEE].visibility
      right_visibility = landmarks[self.RIGHT_KNEE].visibility

      if left_visibility >= right_visibility:
         knee_angle = left_knee_angle,
         hip_idx, knee_idx, ankle_idx, shoulder_idx = 23, 25, 27, 11
      else:
         knee_angle = right_knee_angle
         hip_idx, knee_idx, ankle_idx, shoulder_idx = 24, 26, 28, 12

      back_angle = self.calculate_angle(
         self.get_point(landmarks, shoulder_idx),
         self.get_point(landmarks, hip_idx),
         self.get_point(landmarks, knee_idx),
      )

      key_landmark_visible = landmarks[hip_idx].visibility >= self.MIN_VISIBILITY and landmarks[knee_idx].visibility >= self.MIN_VISIBILITY and landmarks[ankle_idx].visibility >= self.MIN_VISIBILITY

      if key_landmark_visible:
         if knee_angle < self.DOWN_THRESHOLD:
            self.stage = "down"
         if knee_angle >= self.UP_THRESHOLD and self.stage == "down":
            self.stage = "up"
            self.reps += 1
         
      if self.stage == "down":
         depth_status = "GOOD DEPTH" if knee_angle <= self.DOWN_THRESHOLD else "GO DEEPER"
      elif self.stage == "up":
         depth_status = "STANDING"
      else:
         depth_status = "N/A"

      return {
         "reps": self.reps,
         "knee_angle": int(knee_angle),
         "back_angle": int(back_angle),
         "depth_status": depth_status
      }