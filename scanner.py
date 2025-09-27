import cv2
from pyzbar import pyzbar
from typing import Optional

class BarcodeScanner:
    def __init__(self, camera_url: str):
        self.camera_url = camera_url

    def scan(self) -> Optional[str]:
        capture = cv2.VideoCapture(self.camera_url)
        try:
            ret, frame = capture.read()
            while ret:
                ret, frame = capture.read()
                barcodes = pyzbar.decode(frame)
                decoded_text = ""
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    decoded_text = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    label = f"Barcode: {decoded_text},Type:{barcode_type}"
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.imshow("Barcode/QR code reader", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                if decoded_text:
                    return decoded_text
        finally:
            capture.release()
            cv2.destroyAllWindows()
        return None