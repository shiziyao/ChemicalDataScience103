"""
wine_eda.py
-----------
Homework: Exploratory Data Analysis on the Wine dataset.

Goals:
1. Load and inspect the data
2. Perform exploratory analysis
3. Produce some plots for visualisations
4. Apply PCA
5. Apply some simple ML models for classification
6. Summarise results
"""

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix



# Main analysis function
def main():
    # --- 1. Load data ---
    print("Loading dataset...")
    wine = load_wine()
    wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    # add a 'target' column
    wine_df['target']= pd.DataFrame(wine.target, columns=['target'])
    

    # print basic info (shape, first rows, summary statistics)
    print("Shape of dataset;",wine_df.shape)
    print("Top 7 rows of dataset:", wine_df.head(3))
    print("Stats summary of dataframe:", wine_df.describe())
    #print("Info of dataframe:", wine_df.info())
    print("Any null values in dataframe:", wine_df.isnull().sum())

    # --- 2. Basic exploration ---
    # print class distribution and check for missing values as well as duplicates
    wine_df['target'].value_counts()
    print("duplicated rows of dataset:",wine_df[wine_df.duplicated()])
    print("cleaned wine datset (wine_df)")
    wine_df_cleaned=wine_df[~wine_df.duplicated()]
    wine_df_cleaned.head()
    
    # --- 3. Visualisations ---
    # create and save a pairplot using a few selected features
    features=['alcohol', 'malic_acid', 'magnesium','total_phenols', 'flavanoids', 
       'proanthocyanins', 'color_intensity', 'hue','od280/od315_of_diluted_wines', 'proline']
    pairplot_fig=sns.pairplot(wine_df,vars=features)
    pairplot_fig.savefig("wine_features_pairplot.png", dpi=300, bbox_inches="tight")
    plt.show()

    # create and save a boxplot comparing one feature across classes
    ax=sns.boxplot(data=wine_df_cleaned, x='target', y='alcohol')
    ax.set_title("box plot of target against alcohol content")
    plt.savefig("wine_alcohol_boxplot.png", dpi=300, bbox_inches="tight")
    plt.show()

    # plot and save a heatmap (e.g. 'heatmap.png')
    corr=wine_df_cleaned[features].corr()
    ax = sns.heatmap(corr)
    ax.set_title("Heatmap of features")
    plt.savefig("wine_heatmap.png", dpi=400, bbox_inches='tight')
    plt.show()

    # --- 4. Scaling and PCA ---
    # separate features (X) and target (y)
    X= wine_df_cleaned.drop('target', axis=1)
    y= wine_df_cleaned['target']

    # scale the features using StandardScaler
    scaled= StandardScaler()
    X_scaled = scaled.transform(X)

    # apply PCA (2 components)
    pca= PCA(n_components=2)
    scores = pca.transform(X_scaled)

    # create a DataFrame with PCA results and target
    pca_df = pd.DataFrame(scores, columns=['PCA1','PCA2'], index= wine_df_cleaned.index)
    pca_df['target']= wine_df_cleaned['target']

    # plot and save a scatterplot of the first two components (color by target)
    ax=sns.scatterplot(data=pca_df, x='PCA1', y='PCA2', hue='target')
    ax.set_title("Scatterplot for PCA1 and PCA2 with target as hue")
    plt.savefig("PCA scatterplot.png", dpi=400, bbox_inches='tight')
    plt.show()

    # --- 5. Classification models ---
    # Do a random train-test split (20%) 
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

    # Scale training and test features (fit_transform() on X_train, transform() on X_test)
    X_train_scaled=scaled.fit_transform(X_train)
    X_test_scaled= scaled.transform(X_test)

    # Train logistic regression, a decision tree and a random forest (default hyperparameters)
    model_LR= LogisticRegression()
    model_LR.fit(X_train_scaled, y_train)
    y_pred_LR= model_LR.predict(X_test_scaled)

    model_DT= DecisionTreeClassifier()
    model_DT.fit(X_train_scaled,y_train)
    y_pred_DT= model_DT.predict(X_test_scaled)

    model_RF= RandomForestClassifier()
    model_RF.fit(X_train_scaled,y_train)
    y_pred_RF= model_RF.predict(X_test_scaled)

    # Compare the label prediction accuracy of the different models.
    accuracy_LR= accuracy_score(y_test,y_pred_LR)
    accuracy_DT= accuracy_score(y_test, y_pred_DT)
    accuracy_RF= accuracy_score(y_test, y_pred_RF)
    print("accuracy score for Logistic Regression :",accuracy_LR)
    print("accuracy score for Decision Tree :",accuracy_DT)
    print("accuracy score for Random Forest :",accuracy_RF)

    # Train and evaluate the three models on the PCA data.
    X_pca= pca_df.drop('target', axis=1)
    y_pca= pca_df['target']
    X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(X_pca,y_pca,test_size=0.2)

    # Scale training and test features (fit_transform() on X_train, transform() on X_test)
    #X_train_scaled_pca=scaled.fit_transform(X_train_pca)
    #X_test_scaled_pca= scaled.fit_transform(X_test_pca)

    # Train logistic regression, a decision tree and a random forest (default hyperparameters)
    model_LR= LogisticRegression()
    model_LR.fit(X_train_pca, y_train_pca)
    y_pred_LR_pca= model_LR.predict(X_test_pca)

    model_DT= DecisionTreeClassifier()
    model_DT.fit(X_train_pca,y_train_pca)
    y_pred_DT_pca= model_DT.predict(X_test_pca)

    model_RF= RandomForestClassifier()
    model_RF.fit(X_train_pca,y_train_pca)
    y_pred_RF_pca= model_RF.predict(X_test_pca)

    # Compare the label prediction accuracy of the different models.
    accuracy_LR_pca= accuracy_score(y_test_pca,y_pred_LR_pca)
    accuracy_DT_pca= accuracy_score(y_test_pca, y_pred_DT_pca)
    accuracy_RF_pca= accuracy_score(y_test_pca, y_pred_RF_pca)
    print("accuracy score for Logistic Regression with PCA :",accuracy_LR_pca)
    print("accuracy score for Decision Tree with PCA :",accuracy_DT_pca)
    print("accuracy score for Random Forest with PCA :",accuracy_RF_pca)

    
# Entry point
if __name__ == "__main__":
    main()