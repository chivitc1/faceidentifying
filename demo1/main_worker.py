import glob
import os
import re

import cv2
import face_recognition as fr

# predictor_path = 'dlib_data/shape_predictor_5_face_landmarks.dat'
# face_rec_model_path = 'dlib_data/dlib_face_recognition_resnet_model_v1.dat'
known_people_folder = 'images'


cam = cv2.VideoCapture(0)
color_green = (0, 255, 0)
line_width = 2
tolerance = 0.6

def main():
    # face_image = fr.load_image_file('{}/img_20181030_172355.jpg'.format(faces_folder_path))
    # known_face = fr.face_encodings(face_image)

    known_people = scan_known_people(known_people_folder)
    process_this_frame = True
    while True:
        # Capture frame-by-frame
        ret_val, img = cam.read()
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_locations = fr.face_locations(rgb_image, number_of_times_to_upsample=1, model='hog')
        unknown_face_encodings = fr.face_encodings(img)

        # Draw rectangles in detected faces
        # for face_location in face_locations:
        #     cv2.rectangle(img, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color_green, line_width)

        # Rec face
        face_names = []
        for unknown_encoding in unknown_face_encodings:
            for person in known_people.items():
                matches = fr.compare_faces(person[1], unknown_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    name = person[0]
                    face_names.append(name)
                    break

                # distances = fr.face_distance(person[1], unknown_encoding)
                # result = list(distances <= tolerance)
                # if True in result:
                #     face_names.append(person[0])
                #     # print("Recognized: " + person[0])
                #     break

        process_this_frame = not process_this_frame
        # Display the results
        print(face_names)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            # cv2.rectangle(img, (left, top), (right, bottom), color_green, line_width)
            cv2.rectangle(img, (left, top), (right, bottom), color_green,
                          line_width)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Draw captured image to screen
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cam.release()
    cv2.destroyAllWindows()


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def scan_known_people(known_people_folder):
    """
    :param image folder which store subfolder using person's name or identity:
    :return: dict of key = person names, value = list of face encodings for that person
    """
    known_person_names = [d for d in os.listdir(known_people_folder)]

    result = {}
    for name in known_person_names:
        files = [os.path.abspath(f) for f in glob.glob('{}/{}/*.jpg'.format(known_people_folder, name))]
        known_face_encodings = []
        for file in files:
            img = fr.load_image_file(file)
            encodings = fr.face_encodings(img)

            if len(encodings) > 1:
                print("WARNING: More than one face found in {}. Only considering the first face.".format(file))

            if len(encodings) == 0:
                print("WARNING: No faces found in {}. Ignoring file.".format(file))
            else:
                known_face_encodings.append(encodings[0])
        result[name] = known_face_encodings
    return result


if __name__ == '__main__':
    main()