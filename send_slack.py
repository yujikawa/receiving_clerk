import cv2
import os
import setting
from datetime import datetime
from slacker import Slacker

def send_slack(image_path,message='お客様が来社されました'):
    """
    :param image_path:
    :param message:
    :return:
    """
    slacker = Slacker(setting.SLACK_APIKEY)
    slacker.files.upload(image_path, channels=[setting.SLACK_CHANNEL], title='受付情報')
    slacker.chat.post_message(setting.SLACK_CHANNEL, message, as_user=False)


def get_face(frame):
    """
    顔画像取得関数
    :param frame:
    :return:save_image_path
    """
    save_image_path_list = []
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(os.path.join(setting.CASCADE_DIR,"haarcascade_frontalface_alt.xml"))

    # 物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

    if len(facerect) > 0:
        print('顔が検出されました。')
        color = (255, 255, 255)  # 白
        for rect in facerect:
            # 検出した顔を囲む矩形の作成
            #cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color,thickness=2)

            # 現在の時間を取得
            now = datetime.now().strftime('%Y%m%d%H%M%S')
            save_image_path = os.path.join(setting.SAVE_DIR, now + '.jpg')
            # 認識結果の保存
            x = rect[0]
            y = rect[1]
            width = rect[2]+40
            height = rect[3]+40
            dst = frame[y:y + height, x:x + width]
            cv2.imwrite(save_image_path, dst)
            save_image_path_list.append(save_image_path)
    return save_image_path_list


def run():
    """
    カメラ実行
    :return:
    """
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        #frameを表示
        #cv2.imshow('camera capture', frame)
        save_image_path_list = get_face(frame)

        if len(save_image_path_list)>0:
            print(save_image_path_list)
            for save_image_path in save_image_path_list:
                send_slack(save_image_path)
                os.remove(save_image_path)
            break

    #キャプチャを終了
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    run()