from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import tempfile
from .models import RequestData

@csrf_exempt
def generate_video(request):
    if request.method == 'GET':
        text = request.GET.get('text', 'Hello, World!')

        RequestData.objects.create(text=text)

        width, height = 100, 100
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 1
        font_color = (255, 255, 255)
        font_thickness = 2
        fps = 25
        duration = 3

        total_frames = duration * fps
        text_length = cv2.getTextSize(text, font, font_scale, font_thickness)[0][0]

        distance_to_travel = width + text_length
        text_speed = distance_to_travel / total_frames

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.avi')
        temp_filename = temp_file.name
        out = cv2.VideoWriter(temp_filename, fourcc, fps, (width, height))

        text_x_start = width

        for frame_number in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            cv2.putText(frame, text, (int(text_x_start), height // 2), font, font_scale, font_color, font_thickness)
            out.write(frame)

            text_x_start -= text_speed

        out.release()

        response = FileResponse(open(temp_filename, 'rb'), content_type='video/x-msvideo')
        response['Content-Disposition'] = 'attachment; filename=video.avi'
        return response

    else:
        return HttpResponse('Method not allowed', status=405)
