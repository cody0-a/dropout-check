
const ctx = document.getElementById('dropoutChart').getContext('2d');
const dropoutChart = new Chart(ctx, {
    type: 'bar', // Change to 'line', 'pie', etc. as needed
    data: {
        labels: ['2020', '2021', '2022', '2023'], // Years or other categories
        datasets: [{
            label: 'Dropout Rate (%)',
            data: [15, 20, 10, 25], // Replace with your data
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Rate (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Year'
                }
            }
        },
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Dropout Rate Over Years'
            }
        }
    }
});
