from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Label 1 = scam; label 0 = legitimate.
training_data = [
    ("URGENT your bank account will be blocked verify now", 1),
    ("You won a prize claim it by paying a processing fee", 1),
    ("Send your OTP to receive your refund", 1),
    ("Your parcel is held pay this fee using this link", 1),
    ("Your account is suspended click here to verify password", 1),
    ("Congratulations you won a free mobile pay shipping charges", 1),
    ("Investment guaranteed double money in two days", 1),
    ("Send money immediately to unlock your account", 1),
    ("Your KYC expired update details through this link now", 1),
    ("You have won a lottery you never entered", 1),
    ("Share your bank PIN to receive cashback", 1),
    ("Pay a small fee to get your job offer confirmed", 1),
    ("Your UPI account will be blocked click to reactivate", 1),
    ("Claim free gift now by entering card details", 1),
    ("I am a delivery agent pay extra charges through this link", 1),
    ("Your electricity will be disconnected pay immediately", 1),

    ("Your appointment is confirmed for tomorrow at ten", 0),
    ("Hi are we meeting at college today", 0),
    ("Your order has been shipped and is on the way", 0),
    ("Please send me the class notes when you are free", 0),
    ("The team meeting starts at three this afternoon", 0),
    ("Your bill payment was received successfully", 0),
    ("Happy birthday have a wonderful day", 0),
    ("The assignment deadline is Friday", 0),
    ("I will call you after I reach home", 0),
    ("Your appointment reminder is for Monday morning", 0),
    ("The library will close at five today", 0),
    ("Thanks for sharing the project document", 0),
    ("Your food order is being prepared", 0),
    ("The college event starts at nine am", 0),
    ("Please confirm whether you can attend the meeting", 0),
    ("Your monthly statement is available in your bank app", 0),
]

messages = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

model = Pipeline([
    ("text_features", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000)),
])

model.fit(messages, labels)

model_dir = Path("model")
model_dir.mkdir(parents=True, exist_ok=True)

model_path = model_dir / "scam_model.pkl"
joblib.dump(model, model_path)

print("Training completed!")
print(f"Model saved to: {model_path.resolve()}")
print("Prediction labels: 1 = possible scam, 0 = likely legitimate")

# Quick demonstration
test_messages = [
    "Send your OTP now to prevent account blocking",
    "Hi, please send me the project notes",
]

for message, prediction in zip(
    test_messages, model.predict(test_messages)
):
    print(f"\nMessage: {message}")
    print("Prediction:", "POSSIBLE SCAM" if prediction == 1
          else "LIKELY LEGITIMATE")
