import sys
import json
import pickle
import pandas as pd
import os
import traceback

# Add the current directory to the Python path to ensure ipai_data can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from ipai_data import get_ipai_adjustment
    from city_property_types import city_supports_villas
except ImportError:
    # Define fallback functions if the imports fail
    def get_ipai_adjustment(city):
        # Default IPAI values for major cities
        ipai_values = {
            'marrakech': 10.9,
            'tanger': 17.7,
            'casablanca': 15.2,
            'rabat': 12.8,
        }
        city = city.lower()
        ipai_percentage = ipai_values.get(city, 10.5)  # Default to 10.5% if city not found
        return 1 + (ipai_percentage / 100)
    
    def city_supports_villas(city):
        # Cities known to have villa data
        villa_cities = ['casablanca', 'rabat', 'marrakech', 'tanger', 'fes', 'agadir']
        return city.lower() in villa_cities

def debug_print(msg, data=None):
    """Print debug information in JSON format"""
    debug_info = {
        'debug_message': msg,
        'debug_data': data
    }
    print(json.dumps(debug_info), file=sys.stderr)

def load_models():
    """Load the ML models"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(current_dir, 'models')
        
        # Add compatibility handling for scikit-learn version differences
        try:
            with open(os.path.join(models_dir, 'apartment_model.pkl'), 'rb') as f:
                apartment_model = pickle.load(f)
            with open(os.path.join(models_dir, 'villa_model.pkl'), 'rb') as f:
                villa_model = pickle.load(f)
        except AttributeError as e:
            if "'super' object has no attribute '__sklearn_tags__'" in str(e):
                debug_print("Handling scikit-learn version compatibility issue")
                # Use a workaround for scikit-learn version compatibility
                import sklearn
                sklearn.set_config(print_changed_only=False)
                # Try an alternative approach to load models
                import joblib
                apartment_model = joblib.load(os.path.join(models_dir, 'apartment_model.pkl'))
                villa_model = joblib.load(os.path.join(models_dir, 'villa_model.pkl'))
            else:
                raise e
        
        return apartment_model, villa_model
    except Exception as e:
        debug_print("Error loading models", str(e))
        return None, None

def predict_price(input_json):
    """Make a price prediction"""
    try:
        debug_print("Received input", input_json)
        
        # Parse input JSON
        try:
            # Remove any BOM and decode if it's bytes
            if isinstance(input_json, bytes):
                input_json = input_json.decode('utf-8-sig')
            if isinstance(input_json, str):
                # Remove any surrounding quotes if they exist
                input_json = input_json.strip('"\'')
                # Remove BOM if present
                input_json = input_json.lstrip('\ufeff')
                debug_print("Processed input string", input_json)
                data = json.loads(input_json)
            else:
                data = input_json
                
            debug_print("Parsed JSON data", data)
            
        except json.JSONDecodeError as e:
            error_msg = {
                'error': f'Invalid JSON input: {str(e)}',
                'input_received': input_json,
                'input_type': str(type(input_json))
            }
            print(json.dumps(error_msg))
            return

        # Load models
        apartment_model, villa_model = load_models()
        if apartment_model is None or villa_model is None:
            print(json.dumps({'error': 'Failed to load models'}))
            return

        property_type = str(data.get('property_type', '')).lower()
        debug_print("Property type", property_type)
        
        # Create DataFrame for prediction
        input_df = pd.DataFrame({
            'size_sqm': [float(data.get('size_sqm', 0))],
            'bedrooms': [int(data.get('bedrooms', 0))],
            'bathrooms': [int(data.get('bathrooms', 0))],
            'property_age': [int(data.get('property_age', 0))],
            'floor_level': [int(data.get('floor_level', 0))],
            'has_parking': [bool(data.get('has_parking', False))],
            'has_garden': [bool(data.get('has_garden', False))],
            'has_pool': [bool(data.get('has_pool', False))],
            'city': [str(data.get('city', ''))],
            'neighborhood': [str(data.get('neighborhood', ''))]
        })
        
        debug_print("Created input DataFrame", input_df.to_dict('records')[0])
        
        # Check if the city has enough data for predictions
        city = str(data.get('city', '')).lower()
        
        # Cities with enough data for reliable predictions
        CITIES_WITH_RELIABLE_DATA = [
            'agadir', 'casablanca', 'fes', 'marrakech', 'rabat', 'tanger', 'temara', 'tetouan'
        ]
        
        if city not in CITIES_WITH_RELIABLE_DATA:
            error_msg = {
                'error': f"We don't have enough data to make reliable predictions for {city.capitalize()}. Please select a different city."
            }
            print(json.dumps(error_msg))
            return
        
        # Choose model based on property type
        if property_type == 'apartment':
            model = apartment_model
        elif property_type == 'villa':
            # Check if the city supports villas
            city = str(data.get('city', '')).lower()
            if not city_supports_villas(city):
                error_msg = {
                    'error': f"Villa data is not available for {city.capitalize()}. Please select apartment instead."
                }
                print(json.dumps(error_msg))
                return
            model = villa_model
        else:
            print(json.dumps({'error': 'Invalid property type'}))
            return
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        debug_print("Raw prediction", float(prediction))
        
        # Ensure prediction is positive
        prediction = max(0, prediction)
        
        # Get city for IPAI adjustment
        city = str(data.get('city', '')).lower()
        
        # Apply IPAI adjustment based on city
        ipai_factor = get_ipai_adjustment(city)
        adjusted_prediction = prediction * ipai_factor
        debug_print("IPAI adjustment", {"city": city, "ipai_factor": ipai_factor, 
                                      "original": float(prediction), 
                                      "adjusted": float(adjusted_prediction)})
        
        # Calculate both original and adjusted prices
        size_sqm = float(data.get('size_sqm', 0))
        original_total_price = prediction * size_sqm
        adjusted_total_price = adjusted_prediction * size_sqm
        
        debug_print("Price calculations", {
            "original_price_per_sqm": float(prediction),
            "adjusted_price_per_sqm": float(adjusted_prediction),
            "size_sqm": size_sqm,
            "original_total_price": float(original_total_price),
            "adjusted_total_price": float(adjusted_total_price)
        })
        
        result = {
            'original_price': float(original_total_price),
            'predicted_price': float(adjusted_total_price),
            'original_price_per_sqm': float(prediction),
            'price_per_sqm': float(adjusted_prediction),
            'property_type': property_type,
            'ipai_adjustment': ipai_factor,
            'input_summary': {
                'size_sqm': size_sqm,
                'bedrooms': int(data.get('bedrooms', 0)),
                'bathrooms': int(data.get('bathrooms', 0)),
                'city': str(data.get('city', '')),
                'neighborhood': str(data.get('neighborhood', ''))
            }
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        error_info = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        print(json.dumps(error_info))

if __name__ == '__main__':
    try:
        # Get input from command line argument
        if len(sys.argv) > 1:
            debug_print("Command line arguments", sys.argv)
            input_file = sys.argv[1]
            
            # Check if the input is a file path
            if os.path.isfile(input_file):
                with open(input_file, 'r', encoding='utf-8-sig') as f:
                    input_data = f.read()
                debug_print("Read from file", input_data)
                predict_price(input_data)
            else:
                # Fallback to direct JSON input
                predict_price(input_file)
        else:
            print(json.dumps({'error': 'No input data provided'}))
    except Exception as e:
        print(json.dumps({
            'error': f'Script execution error: {str(e)}',
            'traceback': traceback.format_exc()
        })) 