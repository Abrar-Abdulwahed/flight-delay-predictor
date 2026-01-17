document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const carrierSelect = document.getElementById('carrier');
    const airportSelect = document.getElementById('airport');
    const predictBtn = document.getElementById('predict-btn');
    const resultsPlaceholder = document.querySelector('.results-placeholder');
    const resultsContent = document.querySelector('.results-content');
    const predictionPercent = document.getElementById('prediction-percent');
    const meterFill = document.getElementById('meter-fill');
    const predictionText = document.getElementById('prediction-text');

    const API_URL = 'http://127.0.0.1:5005/api';

    // Fetch metadata for dropdowns
    async function fetchMetadata() {
        try {
            const response = await fetch(`${API_URL}/metadata`);
            const data = await response.json();

            data.carriers.forEach(carrier => {
                const option = document.createElement('option');
                option.value = carrier;
                option.textContent = carrier;
                carrierSelect.appendChild(option);
            });

            data.airports.forEach(airport => {
                const option = document.createElement('option');
                option.value = airport;
                option.textContent = airport;
                airportSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching metadata:', error);
            alert('Failed to connect to the prediction server. Please ensure the backend is running.');
        }
    }

    fetchMetadata();

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        predictBtn.classList.add('loading');
        predictBtn.disabled = true;
        predictBtn.querySelector('span').textContent = 'Analyzing Flight Path...';

        const formData = {
            carrier: carrierSelect.value,
            airport: airportSelect.value,
            month: document.getElementById('month').value
        };

        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.status === 'success') {
                displayResult(result.prediction);
            } else {
                alert('Analysis failed: ' + result.error);
            }
        } catch (error) {
            console.error('Error during prediction:', error);
            alert('Server communication error.');
        } finally {
            predictBtn.classList.remove('loading');
            predictBtn.disabled = false;
            predictBtn.querySelector('span').textContent = 'Predict Delay Probability';
        }
    });

    function displayResult(prediction) {
        // Switch views
        resultsPlaceholder.classList.add('hidden');
        resultsContent.classList.remove('hidden');

        // Update values
        const percent = (prediction * 100).toFixed(1);
        predictionPercent.textContent = `${percent}%`;

        // Update meter
        setTimeout(() => {
            meterFill.style.width = `${Math.min(percent, 100)}%`;

            // Color logic based on severity
            if (percent < 10) {
                meterFill.style.background = 'var(--accent-secondary)'; // Green
                predictionText.textContent = 'Minimal risk of delays detected.';
            } else if (percent < 25) {
                meterFill.style.background = '#fbbf24'; // Yellow
                predictionText.textContent = 'Moderate delay probability anticipated.';
            } else {
                meterFill.style.background = '#ef4444'; // Red
                predictionText.textContent = 'High alert: Significant delays expected.';
            }
        }, 100);
    }
});
