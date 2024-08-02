from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, flash
import pandas as pd
from ultralytics import YOLO
import cv2
from getrandomforest import loaded_model
from mongo_config import base_config
from send_detected_email import notify_me, send_email
from score import pred_score
from history import get_history
pd.set_option('display.max_columns', 100)

# Load YOLO model outside the route function
yolo_model = YOLO(r"D:\crime_03_16 (1)\crime_03_16\best.pt")


app = Flask(__name__)
app.secret_key = 'crime'
data, users_collection = base_config()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/users')
def users():
    if 'user_email' in session:
        return render_template('users.html')
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/generalUser')
def general_User():
    return render_template('gen_user.html')


@app.route('/batch_data', methods=['GET'])
def batch_users():
    return render_template('batch_predict.html')


@app.route('/history')
def find_history_in():
    return render_template('history.html')


@app.route('/login', methods=['POST'])
def login_backend():
    email = request.form.get('email')
    password = request.form.get('password')

    user = users_collection.find_one({'email': email, 'password': password})

    if not user:
        message = 'Please enter the correct password and email id.'
        return redirect(url_for('login', message=message))

    session['user_email'] = email
    return redirect(url_for('users'))




@app.route('/signup', methods=['POST'])
def signup_backend():
    name = request.form.get('name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    college_name = request.form.get('college_name')
    password = request.form.get('password')

    existing_user = users_collection.find_one({'email': email})

    if not name or not email or not phone_number or not college_name or not password:
        message = 'Please enter valid field values'
        return redirect(url_for('signup', message=message))

    if existing_user:
        message = 'Email already exists. Try a different email.'
        return render_template('signup.html', message=message)

    new_user = {
        'name': name,
        'email': email,
        'phone_number': phone_number,
        'college_name': college_name,
        'password': password
    }

    users_collection.insert_one(new_user)
    message = 'Account created successfully'
    # Render the signup template with the success message
    return render_template('signup.html', message=message)


@app.route('/generalUser', methods=['POST'])
def general_user_backend():
    state = request.form.get('State')
    district = request.form.get('District')
    year = request.form.get('Year')
    data_subset = data[
        (data["STATE/UT"] == state) & (data["DISTRICT"] == district) & (data["YEAR"] >= 2011) & (
                    data["YEAR"] <= 2023)]
    data_subset = data_subset.groupby(["STATE/UT", "DISTRICT"]).sum().reset_index()
    # Extract features for prediction (excluding STATE/UT, DISTRICT, YEAR, and TOTAL IPC CRIMES)
    X_pred = data_subset.drop(columns=["STATE/UT", "DISTRICT", "YEAR", "TOTAL IPC CRIMES"])
    # Predict for the year 2024
    predicted_crimes_2024 = loaded_model.predict(X_pred)
    predicted_crimes_2024 = int(predicted_crimes_2024)
    Rate, Prediction_score = pred_score(year, predicted_crimes_2024)
    response = {'message': f"Prediction for the Year: {year}, Predicted Crime Number: {Prediction_score}, \n"
                           f"Crime rate: {Rate}"}
    return jsonify(response), 201


@app.route('/batch_data', methods=['POST'])
def process_uploaded_file():
    if 'file' in request.files:
        uploaded_file = request.files['file']
        results = []
        if uploaded_file.filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            df = df[["STATE/UT", "DISTRICT"]]
            for index, row in df.iterrows():
                state = row["STATE/UT"]
                district = row["DISTRICT"]
                data_subset = data[
                    (data["STATE/UT"] == state) & (data["DISTRICT"] == district) & (data["YEAR"] >= 2011) & (
                                data["YEAR"] <= 2023)]
                data_subset = data_subset.groupby(["STATE/UT", "DISTRICT"]).sum().reset_index()
                # Extract features for prediction (excluding STATE/UT, DISTRICT, YEAR, and TOTAL IPC CRIMES)
                X_pred = data_subset.drop(columns=["STATE/UT", "DISTRICT", "YEAR", "TOTAL IPC CRIMES"])
                # Predict for the year 2024
                predicted_crimes_2024 = loaded_model.predict(X_pred)
                predicted_crimes_2024 = int(predicted_crimes_2024)

                if predicted_crimes_2024 < 840:
                    predicted_crimes_2025 = predicted_crimes_2024 + 18
                    predicted_crimes_2026 = predicted_crimes_2024 + 30
                    rate = "low ✅"
                elif 840 < predicted_crimes_2024 < 3875:
                    predicted_crimes_2025 = predicted_crimes_2024 + 76
                    predicted_crimes_2026 = predicted_crimes_2024 + 110
                    rate = "medium 🟡"
                else:
                    predicted_crimes_2025 = predicted_crimes_2024 + 113
                    predicted_crimes_2026 = predicted_crimes_2024 + 143
                    rate = "high ☠️"

                result = {
                    "State/UT": state,
                    "District": district,
                    "Predicted Score 2024": predicted_crimes_2024,
                    "Predicted Score 2025": predicted_crimes_2025,
                    "Predicted Score 2026": predicted_crimes_2026,
                    "Crime Rate": rate
                }
                results.append(result)
        return jsonify(results)

        # return jsonify({"error": "Invalid file format or no file uploaded"}), 400
    return "Invalid file format or no file uploaded", 400


@app.route('/web_cam', methods=['GET'])
def live_weapon_detection():
    # Load YOLO model

    # Capture video from source 0 (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Perform object detection
        results = yolo_model(frame)

        # Check if there are any detections
        if isinstance(results, list) and len(results) > 0:
            first_result = results[0]

            # Check if this result has the expected attribute (e.g., xyxy)
            if hasattr(first_result, 'xyxy') and first_result.xyxy.shape[0] > 0:
                # Iterate through each detection
                for pred in first_result.xyxy:
                    label = int(pred[5])
                    conf = pred[4]
                    if conf > 0.5:  # Set a confidence threshold
                        # send_email("Weapon Detected", "A weapon has been detected in the video stream.")
                        xmin, ymin, xmax, ymax = map(int, pred[:4])
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        cv2.putText(frame, f"Class: {label}, Conf: {conf:.2f}", (xmin, ymin - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with bounding boxes
        cv2.imshow('Object Detection', frame)

        # Check for the 'q' key to exit the loop
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or cv2.getWindowProperty('Object Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("in")
    notify_me()


@app.route('/model_info', methods=['GET'])
def model_info():
    return render_template('model_info.html',
                           state_vs_crime_img="new_state_vs_totalcrimes.png",
                           crime_vs_count_img="new_totalcrime_vs_type.png",
                           year_vs_crime_img="new_year_vs_cases.png",
                           forcasteCrime_img="new_farcaste.png",
                           theft_vsburglary_img="new_theft_vs_burglary.png"
                           )


@app.route('/history', methods=['POST'])
def find_history():
    state = request.form.get('State')
    district = request.form.get('District')
    year = request.form.get('Year')
    history_dict = get_history(data, state, district, int(year))
    response = {'message': f"{history_dict}"}
    return jsonify(response), 201


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    print('hi')
    app.run(debug=True)
