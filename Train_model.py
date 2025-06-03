import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from category_encoders import TargetEncoder
import joblib
import os
import pickle

# Create models directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# Read the dataset
df = pd.read_csv('ml_dataset/morocco_real_estate_prices_with_features.csv')
# Create separate dataframes for apartments and villas
apartment_df = df.copy()
apartment_df['property_type'] = 'apartment'
apartment_df['price'] = apartment_df['apartment_price_sqm']

villa_df = df.copy()
villa_df['property_type'] = 'villa'
villa_df['price'] = villa_df['villa_price_sqm']

# Combine into one dataframe if needed for other operations
combined_df = pd.concat([apartment_df, villa_df])

# Function to create, train, and evaluate a model
def train_and_evaluate_model(data, target_column):
    # Remove rows where target is NaN
    valid_data = data.dropna(subset=[target_column])
    
    # Define features to use
    numeric_features = ['size_sqm', 'bedrooms', 'bathrooms', 'property_age', 'floor_level']
    boolean_features = ['has_parking', 'has_garden', 'has_pool']
    categorical_features = ['city', 'neighborhood']
    
    # Ensure boolean features exist, if not create them with default values
    for feature in boolean_features:
        if feature not in valid_data.columns:
            valid_data[feature] = 0
    
    # Ensure numeric features exist
    for feature in numeric_features:
        if feature not in valid_data.columns:
            # You might need to add default values or skip these features
            valid_data[feature] = 0  # Default value
    
    # Prepare features
    feature_columns = numeric_features + boolean_features + categorical_features
    X = valid_data[feature_columns]
    y = valid_data[target_column]
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create preprocessing steps
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('power', PowerTransformer(method='yeo-johnson', standardize=True))
    ])
    
    categorical_transformer = TargetEncoder()
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features + boolean_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Create the pipeline
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            max_depth=7,
            min_child_weight=1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        ))
    ])
    
    # Train the model
    print(f"\nTraining model for {target_column}...")
    print(f"Number of samples: {len(X_train)}")
    model.fit(X_train, y_train)
    
    # Make predictions
    print(f"Making predictions for {target_column}...")
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance for {target_column}:")
    print(f"Root Mean Squared Error: {rmse:,.2f}")
    print(f"R² Score: {r2:.4f}")
    
    return model

# Train apartment model
print("\n=== Training Apartment Price Model ===")
apartment_model = train_and_evaluate_model(
    data=apartment_df,  # Use the apartment dataframe directly
    target_column='price'
)

# Train villa model
print("\n=== Training Villa Price Model ===")
villa_model = train_and_evaluate_model(
    data=villa_df,  # Use the villa dataframe directly
    target_column='price'
)

# Create models directory if it doesn't exist
os.makedirs('python/models', exist_ok=True)

# Save models in PKL format
print("\nSaving models in PKL format...")
with open('python/models/apartment_model.pkl', 'wb') as f:
    pickle.dump(apartment_model, f)
with open('python/models/villa_model.pkl', 'wb') as f:
    pickle.dump(villa_model, f)

print("\nModels saved successfully!")
print("Models location: ./python/models/")
print("- Apartment model: ./python/models/apartment_model.pkl")
print("- Villa model: ./python/models/villa_model.pkl")

