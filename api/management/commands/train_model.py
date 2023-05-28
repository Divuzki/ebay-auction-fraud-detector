from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pickle

class Command(BaseCommand):
    help = 'Train the shill detector model'

    def add_arguments(self, parser):
        parser.add_argument('data_path', type=str, help='Path to the dataset')

    def handle(self, *args, **options):
        data_path = options['data_path']
        train_shill_detector(data_path)
        self.stdout.write(self.style.SUCCESS('Shill detector model trained successfully.'))

import matplotlib.pyplot as plt

def plot_model_performance(accuracy, precision, recall):
    # Set the performance metrics and corresponding labels
    metrics = ['Accuracy', 'Precision', 'Recall']
    scores = [accuracy, precision, recall]

    # Plot the bar graph
    plt.bar(metrics, scores)
    plt.ylim([0, 1])  # Set the y-axis limits between 0 and 1

    # Add labels and title
    plt.xlabel('Metrics')
    plt.ylabel('Scores')
    plt.title('Model Performance')

    # Display the plot
    plt.show()

def train_shill_detector(data_path):
    # Load the data into a pandas DataFrame
    df = pd.read_csv(data_path)

    # Extract the features you want to use
    X = df[['Bidder_Tendency', 'Bidding_Ratio', 'Successive_Outbidding', 'Last_Bidding',
            'Auction_Bids', 'Starting_Price_Average', 'Early_Bidding', 'Winning_Ratio', 'Auction_Duration']]
    y = df['Class']

    # Split the data into a training and testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Train the model
    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)

    # Evaluate the model on the testing data
    y_pred = logistic_regression.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # then plot the model performance
    plot_model_performance(accuracy, precision, recall)

    # Save the model to a file
    with open('shill_detector.pkl', 'wb') as handle:
        pickle.dump(logistic_regression, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return logistic_regression
