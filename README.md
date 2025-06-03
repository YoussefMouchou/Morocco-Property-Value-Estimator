# Morocco Property Value Estimator

A web application that provides accurate property price estimates for homes in Morocco, leveraging machine learning models and the Bank Al-Maghrib real estate price index (IPAI).

![image](https://github.com/user-attachments/assets/47f48209-c2ce-44dd-b3a8-e7b773526ed2)


## Overview

The Morocco Property Value Estimator is a full-stack web application that helps users estimate the market value of residential properties across major Moroccan cities. The application combines a user-friendly Laravel frontend with powerful Python machine learning models to deliver accurate price predictions based on property characteristics and location data.

## Key Features

- **Property Value Prediction**: Estimate property values based on multiple factors including location, size, age, and amenities
- **City & Neighborhood Selection**: Support for major Moroccan cities including Casablanca, Marrakech, Rabat, Tangier, and more
- **BKAM IPAI Integration**: Incorporates the Bank Al-Maghrib real estate price index (IPAI) to adjust valuations based on current market trends
- **Separate Models**: Different prediction models for apartments and villas to ensure accuracy
- **Responsive Design**: Clean, modern interface that works across desktop and mobile devices

## Technology Stack

### Frontend
- **Laravel**: PHP web framework for the application structure
- **Blade Templates**: For rendering the user interface
- **HTML/CSS/JavaScript**: For the responsive user interface

### Backend
- **Laravel**: Handles form validation, routing, and API communication
- **Python**: Powers the machine learning prediction system
- **Scikit-learn**: For the property value prediction models

### Data
- **BKAM IPAI Data**: Real estate price index from Bank Al-Maghrib (T4 2024)
- **Property Dataset**: Training data for the machine learning models

## Project Structure

```
Morocco-price-estimator/       # Laravel application
├── app/                      
│   └── Http/Controllers/     # Contains PriceEstimatorController
├── resources/
│   └── views/                # Blade templates including price-estimator.blade.php
├── routes/                   # Web routes definition
└── ...                       # Other Laravel files

python/                        # Python ML components
├── predict.py                # Main prediction script
├── ipai_data.py              # BKAM real estate price index data
├── models/                   # Trained ML models
└── requirements.txt          # Python dependencies

ml_dataset/                    # Training data for the models
```

## Setup Instructions

### Prerequisites
- PHP 8.0+ with Composer
- Python 3.8+ with pip
- Laravel 9+
- Web server (Apache/Nginx)

### Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/morocco-price-estimator.git
   cd morocco-price-estimator
   ```

2. **Set up Laravel**
   ```
   composer install
   cp .env.example .env
   php artisan key:generate
   ```

3. **Configure Python path**
   - Open `app/Http/Controllers/PriceEstimatorController.php`
   - Update the `$pythonPath` variable to point to your Python executable

4. **Install Python dependencies**
   ```
   cd python
   pip install -r requirements.txt
   ```

5. **Start the application**
   ```
   cd ..
   php artisan serve
   ```

6. Visit `http://localhost:8000` in your browser

## How It Works

1. Users fill out a form with details about their property (location, size, features, etc.)
2. The form data is validated and sent to the Python prediction engine
3. The appropriate model (apartment or villa) processes the data
4. The prediction is adjusted using the BKAM IPAI data for the specific city
5. Results are displayed to the user with estimated price range

## BKAM IPAI Integration

The application uses the Bank Al-Maghrib real estate price index (IPAI) from T4 2024 to adjust property valuations based on current market trends. Different cities have different adjustment factors:

- Tangier: 17.7%
- Casablanca: 15.2%
- Marrakech: 10.9%
- Rabat: 12.8%
- Agadir: 11.3%
- And more...

## Future Enhancements

- Add support for more cities and neighborhoods
- Implement user accounts to save property estimates
- Create a comparison feature for different properties
- Add historical price trends visualization
- Develop a mobile application

## Contributors

- Youssef Mouchou - Developer
- Fesweb Agence web Maroc - Design & Development

## License

© 2025 Youssef Mouchou | All rights reserved.

---

*This project is for educational and informational purposes only. Property valuations are estimates and should not be considered as official appraisals.*
