fetch('/api/chart-data/')
  .then(res => res.json())
  .then(data => {
    var ctx = document.getElementById("myPieChart");
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.pie.labels,
        datasets: [{
          data: data.pie.data,
          backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
          hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
          hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
        },
        legend: { display: false },
        cutoutPercentage: 80,
      },
    });
  });
