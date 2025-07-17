select
    id as detection_id,
    message_id,
    detected_object_class,
    confidence_score
from raw.image_detections
