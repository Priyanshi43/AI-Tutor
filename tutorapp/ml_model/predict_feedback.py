# predict_feedback.py

from sklearn.tree import DecisionTreeClassifier

# Sample training data
X = [[30], [45], [60], [75], [90]]
y = ["Weak", "Medium", "Medium", "Strong", "Strong"]

model = DecisionTreeClassifier()
model.fit(X, y)

def get_feedback(score):
    return model.predict([[score]])[0]

# ml_model/predict_feedback.py

def get_feedback(percentage):
    if percentage >= 90:
        return "Outstanding performance! You’ve mastered the topic very well."
    elif percentage >= 75:
        return "Great job! You have a strong understanding. Keep it up!"
    elif percentage >= 60:
        return "Good effort! Just a bit more practice will make you perfect."
    elif percentage >= 40:
        return "You’re getting there. Focus more on weak areas."
    elif percentage >= 25:
        return "Needs improvement. Try to review the basics again."
    else:
        return "Don’t be discouraged! Keep practicing and you’ll get better."
    
# tutorapp/ml_model/predict_feedback.py

def generate_feedback_text(score):
    if score >= 80:
        return "Excellent performance! Keep it up!"
    elif score >= 60:
        return "Good job! A little more effort will take you to the top."
    elif score >= 40:
        return "Average performance. Revise the concepts and practice more."
    else:
        return "You need to work hard. Don't give up and keep learning!"

# ✅ NEW FUNCTION for topic-based feedback
def topic_feedback(topic):
    feedback_dict = {
        "Python": "You should revise Python basics like data types, loops, and functions.",
        "AI": "Focus on key AI concepts such as neural networks, supervised vs unsupervised learning.",
        "Maths": "Practice problem-solving and revise core topics like algebra and probability.",
        "DSA": "Work more on arrays, linked lists, and recursion to improve in DSA.",
        "ML": "Study algorithms like Decision Tree, KNN, and Regression. Practice with datasets.",
        "HTML": "Revise basic HTML tags, structure, forms, and semantic elements.",
        "Cloud": "Understand core cloud concepts like IaaS, PaaS, SaaS, and cloud providers.",
        "Networking": "Revise OSI model, IP addressing, protocols (TCP/IP, HTTP).",
        "Database": "Work on SQL queries, normalization, joins, and indexing.",
    }

    # Agar topic match nahi hua to default message
    return feedback_dict.get(topic, "No specific feedback available for this topic. Please revise the core concepts.")

