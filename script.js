// Function to create and configure the chart
function createChart(labels, polarities) {
    const ctx = document.getElementById('polarityChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Polarity',
                data: polarities,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Fetch the CSV file and process the data
fetch('review_with_polarity.csv')
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n');
        const labels = [];
        const polarities = [];

        for (let i = 1; i < rows.length; i++) {
            const [review, polarity] = rows[i].split(',');
            labels.push(review);
            polarities.push(parseFloat(polarity));
        }

        // Call the function to create the chart
        createChart(labels, polarities);

        // Add event listener to download button
        const downloadButton = document.getElementById('downloadButton');
        downloadButton.addEventListener('click', () => {
            // Create a Blob with the CSV data
            const blob = new Blob([data], { type: 'text/csv' });
            
            // Create a download link and trigger the download
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'review_with_polarity.csv';
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
    })
    .catch(error => {
        console.error('Error fetching CSV:', error);
    });
