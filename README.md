# Alzheimer's Risk Assessment Web Application

A comprehensive Flask-based web application for evaluating Alzheimer's disease risk through patient assessment questionnaires. The application collects demographic, lifestyle, and medical history data to calculate a personalized risk score with detailed recommendations.

## Features

- **Multi-step Assessment Form**: Collects data across three categories:
  - Demographics (age, gender, ethnicity, education)
  - Lifestyle factors (BMI, smoking, alcohol, physical activity, diet, sleep)
  - Medical history (family history, chronic conditions)

- **Risk Calculation**: Evidence-based algorithm that calculates:
  - Overall risk score (0-100)
  - Risk level (Low/Moderate/High)
  - Estimated risk percentage
  - Detailed factor breakdown

- **Results Visualization**: 
  - Interactive charts showing risk factor contributions
  - Personalized recommendations
  - Cognitive health tips
  - Risk factor analysis

- **User Experience**:
  - Mobile-responsive design
  - Form data persistence during assessment
  - Progressive form validation
  - Professional medical interface

- **Export Functionality**: Download assessment summary as text file

## Technology Stack

- **Backend**: Flask, Flask-Session
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **Visualization**: Chart.js
- **Styling**: Bootstrap with Replit dark theme
- **Icons**: Font Awesome

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Set environment variables**:
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```
2. **Set up the application**:
   ```bash
   python setup.py
   ```

3. **Run the application**:
   ```bash
   run_app.bat
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Docker Deployment

### Using Docker Compose (Recommended)

**Build the image**:
   ```bash
   docker compose up --build
   ```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| SESSION_SECRET | Secret key for session management | None | Yes |


## File Structure Basic

```
alzheimers-risk-app/
├── templates/                        # HTML templates
│   ├── admin_assessments.html        # Admin Assesments
│   ├── assessment.html               # Assessment form
│   ├── base.html                     # Base template
│   ├── index.html                    # Home page
│   └── results.html                  # Results page
├── app.py                            # Main Flask application
├── crew_agents.py                    # Multi AI agents
├── database.py                       # Database
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Docker configuration
├── LICENSE                           # License
├── main.py                           # Application entry point
├── pyproject.toml                    # Configuration file
├── risk_calculator.py                # Risk assessment algorithm
├── run_app.bat                       # Window run file
├── run_app.sh                        # Shell run file
├── setup.py                          # Setup file
└──  README.md                        # This file
```

## Assessment Categories

### Demographics
- Age (60-90 years)
- Gender (Male/Female)
- Ethnicity (Caucasian/African American/Asian/Other)
- Education Level (None/High School/Bachelor's/Higher)

### Lifestyle Factors
- BMI (15-40)
- Smoking Status (Yes/No)
- Weekly Alcohol Consumption (0-20 units)
- Weekly Physical Activity (0-10 hours)
- Diet Quality Score (0-10)
- Sleep Quality Score (4-10)

### Medical History
- Family History of Alzheimer's
- Cardiovascular Disease
- Diabetes
- Depression
- History of Head Injury
- Hypertension

## Risk Calculation Algorithm

The application uses a weighted scoring system based on medical research:

- **Age**: 25% weight - Risk increases exponentially after 65
- **Medical History**: 30% weight - Family history and chronic conditions
- **Lifestyle**: 20% weight - BMI, smoking, exercise, diet, sleep
- **Education**: 12% weight - Higher education is protective
- **Gender**: 8% weight - Women have slightly higher risk
- **Ethnicity**: 5% weight - Varies by ethnic group

**Risk Levels:**
- Low: 0-29 points
- Moderate: 30-59 points  
- High: 60-100 points

## Usage Tips

1. **Complete Assessment**: Fill out all three sections for accurate results
2. **Honest Responses**: Provide accurate information for meaningful results
3. **Save Progress**: The form automatically saves your progress as you go
4. **Export Results**: Download your assessment summary for your records
5. **Consult Healthcare Provider**: Share results with your doctor for professional guidance

## Security Features

- Session-based data storage (no permanent database)
- Form validation on client and server side
- CSRF protection
- Secure session management
- No personal data persistence

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Troubleshooting

### Common Issues

1. **Application won't start**:
   - Check Python version (3.7+ required)
   - Verify all dependencies are installed
   - Set SESSION_SECRET environment variable

2. **Form data not saving**:
   - Ensure JavaScript is enabled
   - Check browser console for errors
   - Verify session directory permissions

3. **Charts not displaying**:
   - Check internet connection (Chart.js loads from CDN)
   - Verify browser JavaScript support
   - Clear browser cache

### Performance Optimization

- Use Redis for session storage in production
- Enable gzip compression
- Implement caching for static assets
- Use a reverse proxy (nginx) for production deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and informational purposes only. Not intended for medical diagnosis.

## Medical Disclaimer

This assessment tool is for informational purposes only and should not replace professional medical consultation. The risk scores are based on population studies and may not accurately predict individual risk. Always consult with qualified healthcare professionals for medical advice, diagnosis, and treatment decisions.

## Support

For technical issues or questions:
1. Check the troubleshooting section
2. Review the documentation
3. Contact the development team

---

**Version**: 1.0.0  
**Last Updated**: {{ current_date }}
**Minimum Python Version**: 3.7
   