import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import RandomOverSampler
import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import learning_curve
import seaborn as sns
from sklearn.metrics import confusion_matrix
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Load the dataset
dataset_path = 'kitchenDataset.csv'
dataset = pd.read_csv(dataset_path)

# Separate features (X) and labels (y)
X = dataset[['ingredients']]  # Use 'ingredients' as features
y = dataset['meal']  # Predict 'meal'

# Encode the 'ingredients' column
mlb = MultiLabelBinarizer()
X_encoded = pd.DataFrame(mlb.fit_transform(X['ingredients']), columns=mlb.classes_)

# Save the column names during training
column_names = X_encoded.columns.tolist()
joblib.dump(column_names, './column_names_meal_prediction.joblib')

# Encode the target variable 'meal'
label_encoder_y = LabelEncoder()
y_encoded = label_encoder_y.fit_transform(y)

# Use RandomOverSampler to balance the dataset
oversampler = RandomOverSampler(random_state=42)
X_resampled, y_resampled = oversampler.fit_resample(X_encoded, y_encoded)

# Split the resampled dataset into training and testing sets
test_size_percentage = 0.3
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=test_size_percentage, random_state=42, stratify=y_resampled)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the base classifiers
base_classifiers = [
    ('random_forest', RandomForestClassifier(random_state=42)),
    ('svm', SVC(random_state=42)),
    ('logistic_regression', LogisticRegression(random_state=42,solver='liblinear'))
]

# Create the stacking classifier
stacking_classifier = StackingClassifier(estimators=base_classifiers, final_estimator=LogisticRegression(), stack_method='auto')

# Train the stacking classifier
stacking_classifier.fit(X_train_scaled, y_train)

# Save the trained model and encoders
model_data = {'model': stacking_classifier, 'mlb': mlb, 'label_encoder_y': label_encoder_y, 'scaler': scaler}
joblib.dump(model_data, './trained_kitchen_model_meal_prediction.joblib')

# Make predictions on the test set
y_pred = stacking_classifier.predict(X_test_scaled)

# Evaluate the classifier on the test set
accuracy = accuracy_score(y_test, y_pred)
classification_report_text = classification_report(y_test, y_pred, zero_division=1)

# Print the results
print('Accuracy:', accuracy)
print('Classification Report (Test Set):')
print(classification_report_text)


def plot_learning_curve(estimator, X, y, title=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5), save_path=None):
    plt.figure()
    if title is not None:
        plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")

    if save_path is not None:
        plt.savefig(save_path, format='png')

    return plt



# Use the plot_learning_curve function after training the model
title = "Learning Curve (Stacking Classifier)"
cv = 5  # Number of cross-validation folds
plot_learning_curve(stacking_classifier, X_train_scaled, y_train, title=title, cv=cv, n_jobs=-1,save_path="./learning_curve.png")
plt.show()
